CREATE OR REPLACE FUNCTION public.query_samples(
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
		biosample_stable_id text,
		individual_stable_id text,
		description text,
		biosample_status text,
		biosample_status_ontology text,
		individual_age_at_collection_age text,
		individual_age_at_collection_age_group text,
		individual_age_at_collection_age_group_ontology text,
		organ text,
		organ_ontology text,
		tissue text,
		tissue_ontology text,
		cell_type text,
		cell_type_ontology text,
		obtention_procedure text,
		obtention_procedure_ontology text,
		tumor_progression text,
		tumor_progression_ontology text,
		tumor_grade text,
		tumor_grade_ontology text
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
	_join_patient_pedigree_table bool;
	_join_patient_disease_table bool;
BEGIN
	_join_variant_table = FALSE;
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
	IF _filters_converted LIKE '%dat.%' THEN _join_variant_table=TRUE; END IF;
	IF _filters_converted LIKE '%pat_ped.%' THEN _join_patient_pedigree_table=TRUE; END IF;
	IF _filters_converted LIKE '%pat_dis.%' THEN _join_patient_disease_table=TRUE; END IF;

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
			sam.stable_id AS biosample_stable_id,
			pat.stable_id AS individual_stable_id,
			sam.description,
			sam.biosample_status,
			sam.biosample_status_ontology,
			sam.individual_age_at_collection_age,
			sam.individual_age_at_collection_age_group,
			sam.individual_age_at_collection_age_group_ontology,
			sam.organ,
			sam.organ_ontology,
			sam.tissue,
			sam.tissue_ontology,
			sam.cell_type,
			sam.cell_type_ontology,
			sam.obtention_procedure,
			sam.obtention_procedure_ontology,
			sam.tumor_progression,
			sam.tumor_progression_ontology,
			sam.tumor_grade,
			sam.tumor_grade_ontology
		FROM public.sample_w_ontology_terms sam
		INNER JOIN public.patient_w_ontology_terms pat ON pat.id=sam.patient_id
		INNER JOIN public.beacon_dataset_sample_table dataset_sam ON dataset_sam.sample_id=sam.id
		INNER JOIN public.beacon_dataset_table bdataset ON bdataset.id = dataset_sam.dataset_id';
	
	-- Join other tables only if they are necessary	
	IF _join_variant_table THEN
		_query = _query || '
		INNER JOIN public.beacon_data_sample_table dat_sam ON dat_sam.sample_id=sam.id
		INNER JOIN public.beacon_data_table bdat ON bdat.id=dat_sam.data_id';
	END IF;
	
	IF _join_patient_pedigree_table THEN
		_query = _query || '
		INNER JOIN public.patient_pedigree_w_ontology_terms pat_ped ON pat_ped.patient_id=pat.id';
	END IF;
	
	IF _join_patient_disease_table THEN
		_query = _query || '
		INNER JOIN public.patient_disease_w_ontology_terms pat_dis ON pat_dis.patient_id=pat.id';
	END IF;
	
	_query = _query || _where_clause;
	
	_query = _query || ' 
	ORDER BY sam.stable_id,
			pat.stable_id,
			sam.description,
			sam.biosample_status,
			sam.biosample_status_ontology,
			sam.individual_age_at_collection_age,
			sam.individual_age_at_collection_age_group,
			sam.individual_age_at_collection_age_group_ontology,
			sam.organ,
			sam.organ_ontology,
			sam.tissue,
			sam.tissue_ontology,
			sam.cell_type,
			sam.cell_type_ontology,
			sam.obtention_procedure,
			sam.obtention_procedure_ontology,
			sam.tumor_progression,
			sam.tumor_progression_ontology,
			sam.tumor_grade,
			sam.tumor_grade_ontology';
	
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
