
CREATE OR REPLACE FUNCTION public.query_variants(
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
	_include_dataset_responses text,
	_dataset_stable_ids text[],
	_is_authenticated bool,
	_biosample_stable_id text,
	_individual_stable_id text,
	_filters text[],
	_offset integer,
	_limit integer)
    RETURNS TABLE(
		"exists" bool,
		id integer, 
		chromosome text, 
		variant_name text, 
		reference text, 
		alternate text, 
		start integer, 
		"end" integer, 
		variant_type text, 
		variant_cnt integer, 
		call_cnt integer, 
		sample_cnt integer, 
		matching_sample_cnt integer, 
		frequency numeric, 
		dataset_stable_id text
	) 
    LANGUAGE 'plpgsql'
AS $BODY$

-- PRECONDITIONS:
-- _dataset_stable_ids is optional
-- If _is_authenticated=false or _dataset_stable_ids is empty, only PUBLIC datasets will be queried 
--		(regardless there are registered or controlled in _dataset_stable_ids)
-- If _is_authenticated=true, datasets in _dataset_stable_ids will be queried
-- _offset is the number of rows to be skipped
-- _limit is the number of rows to be returned
-- 	If _limit=null & _offset=null, no pagination is applied
-- Expected combinations:
--		* _reference_genome + _chromosome + _alternate_bases + _reference_bases + _start
--		* _reference_genome + _chromosome + _alternate_bases + (_reference_bases) + _start + _end
--		* _reference_genome + _chromosome + (_variant_type) + _start + _end
--		* _reference_genome + _chromosome + (_variant_type) + _start_min + _start_max + _end_min + _end_max

DECLARE
	_query text;
	_where_clause text;
	_filters_converted text;
	_join_patient_table bool;
	_join_sample_table bool;
	_join_patient_pedigree_table bool;
	_join_patient_disease_table bool;
	_manage_datasets_clause text;

BEGIN
	_join_patient_table = FALSE;
	_join_sample_table = FALSE;
	_join_patient_pedigree_table = FALSE;
	_join_patient_disease_table = FALSE;

	SELECT * INTO _filters_converted
	FROM public.parse_filters(_filters);

	-- Aliases used in ontology_term_table
	-- 	'pat'
	-- 	'sam'
	-- 	'pat_ped'
	-- 	'pat_dis'
	-- In the future, we may have filters on beacon_data_table
	
	-- Check what other tables should be joined depending on the filters provided
	-- TODO

	SELECT * INTO _where_clause
	FROM public.add_where_clause_conditions(_variant_type, _start_min, _end, _reference_bases, 
											_alternate_bases, _dataset_stable_ids, _is_authenticated, 
											_biosample_stable_id, _individual_stable_id, _filters_converted);
											
	RAISE NOTICE 'WHERE=%', _where_clause;
	
	IF _where_clause LIKE '%pat.%' OR _where_clause LIKE '%pat_ped.%' OR _where_clause LIKE '%pat_dis.%' THEN 
		_join_sample_table=TRUE;
		_join_patient_table=TRUE; 
	END IF;
	IF _where_clause LIKE '%sam.%' THEN 
		_join_sample_table=TRUE;
	END IF;
	IF _where_clause LIKE '%pat_ped.%' THEN 
		_join_patient_pedigree_table=TRUE; 
	END IF;
	IF _where_clause LIKE '%pat_dis.%' THEN 
		_join_patient_disease_table=TRUE;
	END IF;
	
	SELECT * INTO _manage_datasets_clause
	FROM public.manage_datasets(_include_dataset_responses);
	
	
	RAISE NOTICE 'Parameters:  
		_variant_type=%, 
		_start=%, _start_min=%, _start_max=%, 
		_end=%, _end_min=%, _end_max=%,
		_chromosome=%, _reference_bases=%, _alternate_bases=%, _reference_genome=%, 
		_dataset_stable_ids=%, _is_authenticated=%, 
		_filters=%, _filters_converted=%,
		_biosample_stable_id=%, _individual_stable_id=%,
		_include_dataset_responses=%, 
		_limit=%, _offset=%', 
	_variant_type, _start, _start_min, _start_max, _end, _end_min, _end_max,
	_chromosome, _reference_bases, _alternate_bases, _reference_genome, 
	_dataset_stable_ids, _is_authenticated, _filters, _filters_converted, 
	_biosample_stable_id, _individual_stable_id, 
	_include_dataset_responses,
	_limit, _offset;
	
	---------------------
	-- BUILD THE QUERY --
	---------------------
	_query = '
	WITH vars_found AS (
		SELECT DISTINCT
			CASE WHEN bdat.id IS NOT NULL THEN TRUE ELSE FALSE END AS exists,
			bdat.id AS id,
			bdat.chromosome::text, 
			bdat.variant_id::text, 
			bdat.reference::text, 
			bdat.alternate::text, 
			bdat.start, 
			bdat.end, 
			bdat.type::text, 
			--bdat.sv_length as sv_length, 
			bdat.variant_cnt as variant_cnt, 
			bdat.call_cnt as call_cnt, 
			bdat.sample_cnt as sample_cnt, 
			bdat.matching_sample_cnt as matching_sample_cnt, 
			bdat.frequency as frequency,
			bdataset.stable_id::text as dataset_stable_id
		FROM public.beacon_data_table bdat
		INNER JOIN public.beacon_dataset_table bdataset ON bdataset.id=bdat.dataset_id';
		
	IF _join_sample_table THEN
		_query = _query || '
		INNER JOIN public.beacon_data_sample_table dat_sam ON dat_sam.data_id=bdat.id
		INNER JOIN public.beacon_sample_table sam ON sam.id=dat_sam.sample_id';
	END IF;
	IF _join_patient_table THEN
		_query = _query || '
		INNER JOIN public.patient_table pat ON pat.id=sam.patient_id';
	END IF;
	IF _join_patient_pedigree_table THEN
		_query = _query || '
		INNER JOIN public.patient_pedigree_table pat_ped ON pat_ped.patient_id=pat.id';
	END IF;
	IF _join_patient_disease_table THEN
		_query = _query || '
		INNER JOIN public.patient_disease_table pat_dis ON pat_dis.patient_id=pat.id';
	END IF;
		
	_query = _query || _where_clause;
	
	_query = _query || '
	)
	SELECT 
		COALESCE(vars_found.exists, FALSE) AS exists,
		vars_found.id,
		vars_found.chromosome::text, 
		vars_found.variant_id::text, 
		vars_found.reference::text, 
		vars_found.alternate::text, 
		vars_found.start, 
		vars_found.end, 
		vars_found.type::text, 
		--bdat.sv_length as sv_length, 
		vars_found.variant_cnt, 
		vars_found.call_cnt, 
		vars_found.sample_cnt, 
		vars_found.matching_sample_cnt, 
		vars_found.frequency,
		coalesce(vars_found.dataset_stable_id, bdataset.stable_id)::text as dataset_stable_id
	' || _manage_datasets_clause;

	_query = _query || '
	ORDER BY 
		vars_found.id,
		vars_found.chromosome, 
		vars_found.variant_id, 
		vars_found.reference, 
		vars_found.alternate, 
		vars_found.start, 
		vars_found."end", 
		vars_found."type", 
		vars_found.dataset_stable_id';

	-- Apply pagination
	_query = _query || '
		LIMIT $15 OFFSET $16';

	RAISE NOTICE '_query: %', _query;

	RETURN QUERY EXECUTE _query
	USING _variant_type, _start, _chromosome, _reference_bases, _alternate_bases, 
		_reference_genome, _dataset_stable_ids, _end, _start_min, _start_max, _end_min, _end_max, 
		_biosample_stable_id, _individual_stable_id, _limit, _offset;
	-- #1=_variant_type, #2=_start, #3=_chromosome, #4=_reference_bases, #5=_alternate_bases, 
	-- #6=_reference_genome, #7=_dataset_stable_ids, #8=_end, #9=_start_min, #10=_start_max, 
	-- #11=_end_min, #12=_end_max, #13=_biosample_stable_id, #14=_individual_stable_id,
	-- #15=_limit, #16=_offset
END
$BODY$;
