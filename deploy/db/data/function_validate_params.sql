
--DROP FUNCTION public.validate_params(text,integer,integer,integer,integer,integer,integer,character varying,text,text,text,text,text,integer,integer)
CREATE OR REPLACE FUNCTION public.validate_params(
	INOUT _variant_type text,
	INOUT _start integer,
	INOUT _start_min integer,
	INOUT _start_max integer,
	INOUT _end integer,
	INOUT _end_min integer,
	INOUT _end_max integer,
	INOUT _chromosome character varying,
	INOUT _reference_bases text,
	INOUT _alternate_bases text,
	INOUT _reference_genome text,
	INOUT _dataset_ids text,
	INOUT _filters text,
	IN _skip integer,
	INOUT _limit integer,
	OUT _filters_converted text,
	OUT _offset integer,
	OUT _join_variant_table bool)
    LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
	_check_variant_params bool;
BEGIN
	-- _filters format: comma separated list of CURIEs
	-- 		Example: NCIT:C46113,NCIT:C17600,GAZ:00001086
	-- _dataset_ids: comma separated list of IDs
	--		Example: 1,2,3

	--------------------
	-- INIT OF PARAMS --
	--------------------
	-- Initialize text parameters
	IF _variant_type IS NOT NULL AND _variant_type = 'null' THEN _variant_type = null; END IF;
	IF _chromosome IS NOT NULL AND _chromosome = 'null' THEN _chromosome = null; END IF;
	IF _reference_bases IS NOT NULL AND _reference_bases = 'null' THEN _reference_bases = null; END IF;
	IF _alternate_bases IS NOT NULL AND _alternate_bases = 'null' THEN _alternate_bases = null; END IF;
	IF _reference_genome IS NOT NULL AND _reference_genome = 'null' THEN _reference_genome = null; END IF;
	IF _dataset_ids IS NOT NULL AND _dataset_ids = 'null' THEN _dataset_ids = null; END IF;
	IF _filters IS NOT NULL AND _filters = 'null' THEN _filters = null; END IF;
	_join_variant_table = FALSE;
	------------------------
	-- END INIT OF PARAMS --
	------------------------
	
	----------------
	-- PAGINATION --
	----------------
	-- If pagination is not provided, set to default values
	IF _skip IS NULL THEN _offset=0; END IF;
	IF _limit IS NULL THEN _limit=10; END IF;
	
	-- Calculate OFFSET
	-- _offset, number of rows to be skipped vs _skip, number of pages to be skipped
	IF _skip IS NOT NULL THEN
		_offset = _limit * _skip;
	END IF;
	
	-- _limit=0 means no pagination -> all rows will be returned
	IF _limit = 0 THEN 
		_limit = null; 
		_offset = 0;
	END IF;
	--------------------
	-- END PAGINATION --
	--------------------
	
	IF _start IS NOT NULL OR _end IS NOT NULL 
		OR _start_min IS NOT NULL OR _start_max IS NOT NULL OR _end_min IS NOT NULL OR _end_max IS NOT NULL
		OR _chromosome IS NOT NULL OR _reference_genome IS NOT NULL OR _variant_type IS NOT NULL
		OR _reference_bases IS NOT NULL OR _alternate_bases IS NOT NULL
	THEN
			-- Check the variant parameters
			_check_variant_params = TRUE;
			_join_variant_table = TRUE;
	END IF;	

	IF _check_variant_params THEN
		-- start: Precise start coordinate position, allele locus (0-based, inclusive).
		-- end: Precise end coordinate (0-based, exclusive).
		--
		-- start only:
		--   - for single positions, e.g. the start of a specified sequence alteration
		--     where the size is given through the specified alternate_bases
		--   - typical use are queries for SNV and small InDels
		--   - the use of "start" without an "end" parameter requires the use of
		--     "reference_bases"
		--
		-- start and end:
		--   - special use case for exactly determined structural changes
		--
		-- start_min + start_max + end_min + end_max
		--   - for querying imprecise positions (e.g. identifying all structural
		--     variants starting anywhere between start_min <-> start_max, and ending
		--     anywhere between end_min <-> end_max
		--   - single or double sided precise matches can be achieved by setting
		--     start_min = start_max XOR end_min = end_max

		IF _chromosome IS NULL THEN RAISE EXCEPTION '_chromosome is required'; END IF;
		--IF _alternate_bases IS NULL AND _variant_type IS NULL THEN RAISE EXCEPTION 'Either _alternate_bases or _variant_type is required'; END IF;
		IF _reference_genome IS NULL THEN RAISE EXCEPTION '_reference_genome is required'; END IF;

		IF _start IS NULL
		THEN
			-- _start is null but _end is provided
			IF _end IS NOT NULL
				THEN RAISE EXCEPTION '_start is required if _end is provided';
			END IF;
			-- _start, _start_min, _start_max, _end_min, _end_max are null
			IF _start_min IS NULL AND _start_max IS NULL AND _end_min IS NULL AND _end_max IS NULL
				THEN RAISE EXCEPTION 'Either _start or all of _start_min, _start_max, _end_min and _end_max are required';
			-- _start is null and some of _start_min, _start_max, _end_min or _end_max are null too
			ELSIF _start_min IS NULL OR _start_max IS NULL OR _end_min IS NULL OR _end_max IS NULL
				THEN RAISE EXCEPTION 'All of _start_min, _start_max, _end_min and _end_max are required';
			END IF;
		-- _start is not null and either _start_min, _start_max, _end_min or _end_max has been provided too
		ELSIF _start_min IS NOT NULL OR _start_max IS NOT NULL OR _end_min IS NOT NULL OR _end_max IS NOT NULL
			THEN RAISE EXCEPTION '_start cannot be provided at the same time as _start_min, _start_max, _end_min and _end_max';
		ELSIF _end IS NULL AND _reference_bases='N' 
			THEN RAISE EXCEPTION '_reference_bases cannot be N if _end is missing';
		END IF;

		IF _start IS NOT NULL AND _end IS NULL AND _reference_bases IS NULL
		THEN RAISE EXCEPTION '_reference_bases is required if _start is provided and _end is missing';
		END IF;

		_variant_type = upper(_variant_type);
		_reference_bases=upper(_reference_bases);
		_alternate_bases=upper(_alternate_bases);
		_reference_genome=lower(_reference_genome);

		IF _variant_type IS NOT NULL THEN
		  IF _variant_type NOT IN ('DEL','DUP','INS','INV','CNV','DUP:TANDEM','DEL:ME','INS:ME')
			THEN RAISE EXCEPTION 'Structural variant type not implemented yet';
		  --ELSIF _alternate_bases IS NOT NULL AND _alternate_bases!='N'
			--THEN RAISE EXCEPTION 'If _variant_type provided, _alternate_bases must be N or null';
		  END IF;
		END IF;

		IF _variant_type IS NULL AND _alternate_bases IS NULL
		  --THEN RAISE EXCEPTION 'Either _variant_type or _alternate_bases is mandatory';
		  THEN _alternate_bases='*';
		END IF;
		IF _alternate_bases='N' THEN _alternate_bases='*'; END IF; -- Look for any variant
	END IF;
	
	-- Prepare filters
	SELECT string_agg(q.my_filter, ' AND ') INTO _filters_converted
	FROM (
		select target_table_alias || '.' || column_name || '=' || quote_literal(column_value) as my_filter
		from (
			SELECT trim(split_part(filter_term,':',1)) AS ontology, 
				trim(split_part(filter_term,':',2)) AS term
			FROM regexp_split_to_table(trim(_filters), ',') AS filter_term
		)q
		LEFT JOIN public.ontology_term_table ot ON ot.ontology=q.ontology AND ot.term=q.term
	)q;
	
	-- Aliases used in ontology_term_table_
	-- 	'pat'
	-- 	'sam'
	-- 	'pat_ped'
	-- 	'pat_dis'
	-- In the future, we may have filters on beacon_data_table
-- 	IF _filters_converted LIKE '%dat.' THEN _join_variant_table=TRUE; END IF;
-- 	IF _filters_converted LIKE '%pat_ped.' THEN _join_patient_pedigree_table=TRUE; END IF;
-- 	IF _filters_converted LIKE '%pat_dis.' THEN _join_patient_disease_table=TRUE; END IF;
-- 	IF _filters_converted LIKE '%pat.' THEN _join_patient_table=TRUE; END IF;

-- 	RETURN SELECT ROW(_variant_type,
-- 		_start,
-- 		_start_min,
-- 		_start_max,
-- 		_end,
-- 		_end_min,
-- 		_end_max,
-- 		_chromosome,
-- 		_reference_bases,
-- 		_alternate_bases,
-- 		_reference_genome,
-- 		_dataset_ids,
-- 		_skip,
-- 		_limit,
-- 		_filters_converted);

END
$BODY$;