-- DROP FUNCTION public.query_patients(text, integer, integer, integer, integer, integer, integer, character varying, text, text, text, text, text, text);

CREATE OR REPLACE FUNCTION public.query_patients(
	_variant_type text,
	_start integer,
	_start_min integer,
	_start_max integer,
	_end integer,
	_end_min integer,
	_end_max integer,
	_chromosome character varying,
	_reference_bases text,
	_alternate_bases text,
	_reference_genome text,
	_dataset_ids text,
	_individual_stable_id text,
	_filters text)
    RETURNS TABLE(
		individual_stable_id text,
		sex text,
		ethnicity text,
		geographic_origin text,
		disease_id text,
		disease_age_of_onset_age text,
		disease_age_of_onset_age_group text,
		disease_stage text,
		disease_family_history bool,
		pedigree_stable_id text,
		pedigree_role text,
		pedigree_no_individuals_tested int,
		pedigree_disease_id text
	) 
    LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
	_query text;
	_check_variant_params bool;
	_filters_converted text;
	_join_variant_table bool;
BEGIN
	-- _filters format: comma separated list of CURIEs
	-- 		Example: NCIT:C46113,NCIT:C17600,GAZ:00001086
	-- _dataset_ids: comma separated list of IDs
	--		Example: 1,2,3

	-- Initialize String parameters
	IF _variant_type IS NOT NULL AND _variant_type = 'null' THEN _variant_type = null; END IF;
	IF _chromosome IS NOT NULL AND _chromosome = 'null' THEN _chromosome = null; END IF;
	IF _reference_bases IS NOT NULL AND _reference_bases = 'null' THEN _reference_bases = null; END IF;
	IF _alternate_bases IS NOT NULL AND _alternate_bases = 'null' THEN _alternate_bases = null; END IF;
	IF _reference_genome IS NOT NULL AND _reference_genome = 'null' THEN _reference_genome = null; END IF;
	IF _dataset_ids IS NOT NULL AND _dataset_ids = 'null' THEN _dataset_ids = null; END IF;
	IF _individual_stable_id IS NOT NULL AND _individual_stable_id = 'null' THEN _individual_stable_id = null; END IF;
	IF _filters IS NOT NULL AND _filters = 'null' THEN _filters = null; END IF;

	-- Initialize boolean variables
	_filters_converted = FALSE;
	_join_variant_table = FALSE;
	
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
			FROM regexp_split_to_table(trim('NCIT:C46113,NCIT:C17600,GAZ:00001086'), ',') AS filter_term
		)q
		LEFT JOIN public.ontology_term_table ot ON ot.ontology=q.ontology AND ot.term=q.term
	)q;
	
	-- Aliases used in ontology_term_table_
	-- 	'pat'
	-- 	'sam'
	-- 	'pat_ped'
	-- 	'pat_dis'
	-- In the future, we may have filters on beacon_data_table
	IF _filters_converted LIKE '%dat.' THEN _join_variant_table=TURE; END IF;

	---------------------
	---------------------
	-- BUILD THE QUERY --
	---------------------
	---------------------

	_query = '
		SELECT DISTINCT
			pat.stable_id AS individual_id,
			pat.sex AS sex,
			pat.ethnicity AS ethnicity,
			pat.geographic_origin AS geographic_origin,
			pat_dis.disease AS disease_id,
			pat_dis.age AS disease_age_of_onset_age,
			pat_dis.age_group AS disease_age_of_onset_age_group,
			pat_dis.stage AS disease_stage,
			pat_dis.family_history AS disease_family_history,
			ped.stable_id AS pedigree_id,
			pat_ped.pedigree_role AS pedigree_role,
			pat_ped.number_of_individuals_tested AS pedigree_no_individuals_tested,
			pat_ped.disease AS pedigree_disease_id
		FROM public.patient_table pat
		LEFT JOIN public.patient_pedigree_table pat_ped ON pat_ped.patient_id=pat.id
		LEFT JOIN public.pedigree_table ped ON ped.id=pat_ped.pedigree_id
		LEFT JOIN public.patient_disease_table pat_dis ON pat_dis.patient_id=pat.id
		INNER JOIN public.beacon_sample_table sam ON sam.patient_id=pat.id
		INNER JOIN public.beacon_dataset_sample_table dataset_sam ON dataset_sam.sample_id=sam.id
		';
	
	IF _join_variant_table THEN
		_query = _query || '
		INNER JOIN public.beacon_data_sample_table dat_sam ON dat_sam.sample_id=sam.id
		INNER JOIN public.beacon_data_table dat ON dat.id=dat_sam.data_id
		';
	END IF;
	
	_query = _query || '
		WHERE
		';

	-- Datasets
	_query = _query || ' dataset_sam.dataset_id = ANY (string_to_array($7, '','')::int[])';
	
	IF _individual_stable_id IS NOT NULL THEN
		_query =  _query || ' AND ' || '
		pat.stable_id=$13
		';
	END IF;
	
	IF _filters IS NOT NULL THEN
		_query = _query || ' AND ' ||
		(SELECT string_agg(q.my_filter, ' AND ') as my_filter
		FROM (
			select target_table_alias || '.' || column_name || '=' || quote_literal(column_value) as my_filter
			from (
				SELECT trim(split_part(filter_term,':',1)) as ontology, 
					trim(split_part(filter_term,':',2)) as term
				FROM regexp_split_to_table(trim(_filters), ',') AS filter_term
			)q
			LEFT JOIN public.ontology_term_table ot ON ot.ontology=q.ontology and ot.term=q.term
		)q);
	END IF;

	IF _join_variant_table THEN
		IF _variant_type IN ('DUP','DEL','INS','INV','CNV','DUP:TANDEM','DEL:ME','INS:ME') THEN
			_query = _query || ' bdat.type=$1 AND';
		END IF;

		raise notice '_alternate_bases: %', _alternate_bases;
		raise notice '_dataset_ids: %', _dataset_ids;

		IF _start_min IS NOT NULL THEN
			_query = _query || ' bdat.start >= $9 AND bdat.start < $10
							AND bdat.end >= $11	AND bdat.end < $12 AND
			 ';
		ELSIF _alternate_bases != '*' OR (_alternate_bases = '*' AND _end IS NULL)
			OR (_alternate_bases IS NULL AND _variant_type IS NOT NULL) THEN
		  -- Looking for an exact match
			_query = _query || ' bdat.start = $2 AND';
		END IF;

		IF _end IS NOT NULL THEN
		  -- Remember that end is exclusive
		  IF _alternate_bases = '*' THEN
			 -- Looking for any variant within this range
			_query = _query || ' (bdat.start >= $2 AND bdat.start < $8 ' ||
			 'OR bdat.end >= $2 AND bdat.end < $8) AND
			 ';
		  ELSE
			-- Looking for an exact match
			  _query = _query || ' bdat.end = ($8-1) AND
			 ';
			END IF;
		END IF;

		-- Chromosome
		_query = _query || ' bdat.chromosome=$3 AND';

		-- Reference parameter is not mandatory
		IF _reference_bases IS NOT NULL AND _reference_bases!='N' THEN
			_query=_query || ' bdat.reference=$4 AND';
		END IF;

		-- Alternate bases
		IF _alternate_bases IS NOT NULL THEN
		  IF _variant_type='INS' THEN
			  _query = _query || ' bdat.alternate like bdat.reference || $5 || ''%'' AND';
			ELSIF _alternate_bases NOT IN ('N','*') THEN
			  _query = _query || ' bdat.alternate=$5 AND';
			END IF;
		END IF;

		-- Convert reference_genome column to lower case
		_query = _query || ' lower(bdataset.reference_genome)=$6 AND';
	END IF;

	_query = _query || ' 
	ORDER BY pat.stable_id,
			pat.sex,
			pat.ethnicity,
			pat.geographic_origin,
			pat_dis.disease,
			pat_dis.age,
			pat_dis.age_group,
			pat_dis.stage,
			pat_dis.family_history,
			ped.stable_id,
			pat_ped.pedigree_role,
			pat_ped.number_of_individuals_tested,
			pat_ped.disease';

	RAISE NOTICE '_query: %', _query;

	RETURN QUERY EXECUTE _query
	USING _variant_type, _start, _chromosome, _reference_bases, _alternate_bases, 
		_reference_genome, _dataset_ids, _end, _start_min, _start_max, _end_min, _end_max, 
		_individual_stable_id;
	-- #1=_variant_type, #2=_start, #3=_chromosome, #4=_reference_bases, #5=_alternate_bases, 
	-- #6=_reference_genome, #7=_dataset_ids, #8=_end, #9=_start_min, #10=_start_max, 
	-- #11=_end_min, #12=_end_max, #13=_individual_stable_id
END
$BODY$;

ALTER FUNCTION public.query_patients(text, integer, integer, integer, integer, integer, integer, character varying, text, text, text, text, text, text)
    OWNER TO microaccounts_dev;


