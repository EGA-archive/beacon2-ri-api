
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
	_dataset_stable_ids text[],
	_is_authenticated bool,
	_biosample_stable_id text,
	_individual_stable_id text,
	_filters text[],
	_offset integer,
	_limit integer)
    RETURNS TABLE(
		individual_stable_id text,
		sex text,
		sex_ontology text,
		ethnicity text,
		ethnicity_ontology text,
		geographic_origin text,
		geographic_origin_ontology text,
		disease_id text,
		disease_id_ontology text,
		disease_age_of_onset_age text,
		disease_age_of_onset_age_group text,
		disease_age_of_onset_age_group_ontology text,
		disease_stage text,
		disease_stage_ontology text,
		disease_family_history bool,
		pedigree_stable_id text,
		pedigree_role text,
		pedigree_role_ontology text,
		pedigree_no_individuals_tested int,
		pedigree_disease_id text,
		pedigree_disease_id_ontology text
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
	_join_variant_table bool;
BEGIN
	_join_variant_table = FALSE;

	SELECT * INTO _filters_converted
	FROM public.parse_filters(_filters);

	-- Aliases used in ontology_term_table
	-- 	'pat'
	-- 	'sam'
	-- 	'pat_ped'
	-- 	'pat_dis'
	-- In the future, we may have filters on beacon_data_table
	
	-- Check what other tables should be joined depending on the filters provided
	IF _filters_converted LIKE '%dat.%' THEN _join_variant_table=TRUE; END IF;
	
	SELECT * INTO _where_clause
	FROM public.add_where_clause_conditions(_variant_type, _start_min, _end, _reference_bases, 
											_alternate_bases, _dataset_stable_ids, _is_authenticated, 
											_biosample_stable_id, _individual_stable_id, _filters_converted);
											
	RAISE NOTICE 'WHERE=%', _where_clause;
											
	IF _where_clause LIKE '%bdat.%' THEN _join_variant_table=TRUE; END IF;
	
	RAISE NOTICE 'Parameters:  
		_variant_type=%, 
		_start=%, _start_min=%, _start_max=%, 
		_end=%, _end_min=%, _end_max=%,
		_chromosome=%, _reference_bases=%, _alternate_bases=%, _reference_genome=%, 
		_dataset_stable_ids=%, _is_authenticated=%, 
		_filters=%, _filters_converted=%,
		_biosample_stable_id=%, _individual_stable_id=%,
		_limit=%, _offset=%, _join_variant_table=%', 
	_variant_type, _start, _start_min, _start_max, _end, _end_min, _end_max,
	_chromosome, _reference_bases, _alternate_bases, _reference_genome, 
	_dataset_stable_ids, _is_authenticated, _filters, _filters_converted, 
	_biosample_stable_id, _individual_stable_id, 
	_limit, _offset, _join_variant_table;
	
	---------------------
	-- BUILD THE QUERY --
	---------------------
	_query = '
		SELECT DISTINCT
			pat.stable_id AS individual_id,
			pat.sex AS sex,
			pat.sex_ontology AS sex_ontology,
			pat.ethnicity AS ethnicity,
			pat.ethnicity_ontology AS ethnicity_ontology,
			pat.geographic_origin AS geographic_origin,
			pat.geographic_origin_ontology AS geographic_origin_ontology,
			pat_dis.disease AS disease_id,
			pat_dis.disease_ontology AS disease_id_ontology,
			pat_dis.age AS disease_age_of_onset_age,
			pat_dis.age_group AS disease_age_of_onset_age_group,
			pat_dis.age_group_ontology AS disease_age_of_onset_age_group_ontology,
			pat_dis.stage AS disease_stage,
			pat_dis.stage_ontology AS disease_stage_ontology,
			pat_dis.family_history AS disease_family_history,
			ped.stable_id AS pedigree_id,
			pat_ped.pedigree_role AS pedigree_role,
			pat_ped.pedigree_role_ontology AS pedigree_role_ontology,
			pat_ped.number_of_individuals_tested AS pedigree_no_individuals_tested,
			pat_ped.disease AS pedigree_disease_id,
			pat_ped.disease_ontology AS pedigree_disease_id_ontology
		FROM public.patient_w_ontology_terms pat 
		INNER JOIN public.beacon_sample_table sam ON sam.patient_id=pat.id
		INNER JOIN public.beacon_dataset_sample_table dataset_sam ON dataset_sam.sample_id=sam.id
		INNER JOIN public.beacon_dataset_table bdataset ON bdataset.id = dataset_sam.dataset_id';
	
	-- Join other tables only if they are necessary
	IF _join_variant_table THEN
		_query = _query || '
		INNER JOIN public.beacon_data_sample_table dat_sam ON dat_sam.sample_id=sam.id
		INNER JOIN public.beacon_data_table bdat ON bdat.id=dat_sam.data_id AND bdat.dataset_id=bdataset.id';
	END IF;
	
	-- Add LEFT JOINs
	_query = _query || '
		LEFT JOIN public.patient_pedigree_w_ontology_terms pat_ped ON pat_ped.patient_id=pat.id
		LEFT JOIN public.pedigree_table ped ON ped.id=pat_ped.pedigree_id
		LEFT JOIN public.patient_disease_w_ontology_terms pat_dis ON pat_dis.patient_id=pat.id';

	_query = _query || _where_clause;
	
	_query = _query || ' 
		ORDER BY pat.stable_id,
			pat.sex,
			pat.sex_ontology,
			pat.ethnicity,
			pat.ethnicity_ontology,
			pat.geographic_origin,
			pat.geographic_origin_ontology,
			pat_dis.disease,
			pat_dis.disease_ontology,
			pat_dis.age,
			pat_dis.age_group,
			pat_dis.age_group_ontology,
			pat_dis.stage,
			pat_dis.stage_ontology,
			pat_dis.family_history,
			ped.stable_id,
			pat_ped.pedigree_role,
			pat_ped.pedigree_role_ontology,
			pat_ped.number_of_individuals_tested,
			pat_ped.disease,
			pat_ped.disease_ontology';
	
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
