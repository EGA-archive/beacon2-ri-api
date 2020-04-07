-- DROP FUNCTION public.query_patients(text, integer, integer, integer, integer, integer, integer, character varying, text, text, text, text, text, text, text, integer, integer);

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
	_biosample_stable_id text,
	_individual_stable_id text,
	_filters text,
	_skip integer,
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

DECLARE
	_query text;
	_filters_converted text;
	_join_variant_table bool;
	_offset integer;
BEGIN
	--------------------
	-- INIT OF PARAMS --
	--------------------
	-- Initialize text parameters
	IF _biosample_stable_id IS NOT NULL AND _biosample_stable_id = 'null' THEN _biosample_stable_id = null; END IF;
	IF _individual_stable_id IS NOT NULL AND _individual_stable_id = 'null' THEN _individual_stable_id = null; END IF;

	------------------------
	-- END INIT OF PARAMS --
	------------------------
	
	RAISE NOTICE 'Parameters before validation:  
		_variant_type=%, 
		_start=%, _start_min=%, _start_max=%, 
		_end=%, _end_min=%, _end_max=%,
		_chromosome=%, _reference_bases=%, _alternate_bases=%,
		_reference_genome=%, _dataset_ids=%,
		_limit=%, _offset=%,
		_filters=%, _filters_converted=%,
		_join_variant_table=%', 
		_variant_type, _start, _start_min, _start_max, _end, _end_min, _end_max,
		_chromosome, _reference_bases, _alternate_bases, _reference_genome, _dataset_ids,
		_limit, _offset, _filters, _filters_converted, _join_variant_table;
	
	SELECT vp._variant_type, 
		vp._start, vp._start_min, vp._start_max, 
		vp._end, vp._end_min, vp._end_max,
		vp._chromosome, vp._reference_bases, vp._alternate_bases, 
		vp._reference_genome, vp._dataset_ids,
		vp._limit, vp._offset, 
		vp._filters_converted, vp._filters,
		vp._join_variant_table
	INTO _variant_type, 
		_start, _start_min, _start_max, 
		_end, _end_min, _end_max,
		_chromosome, _reference_bases, _alternate_bases, 
		_reference_genome, _dataset_ids,
		_limit, _offset, 
		_filters_converted, _filters,
		_join_variant_table
	FROM public.validate_params(_variant_type, _start, _start_min, _start_max, _end, _end_min, _end_max,
		_chromosome, _reference_bases, _alternate_bases, _reference_genome, _dataset_ids, _filters, 
		_skip, _limit
	)vp;
	
	RAISE NOTICE 'Parameters after validation:  
		_variant_type=%, 
		_start=%, _start_min=%, _start_max=%, 
		_end=%, _end_min=%, _end_max=%,
		_chromosome=%, _reference_bases=%, _alternate_bases=%,
		_reference_genome=%, _dataset_ids=%,
		_limit=%, _offset=%,
		_filters=%, _filters_converted=%,
		_join_variant_table=%', 
		_variant_type, _start, _start_min, _start_max, _end, _end_min, _end_max,
		_chromosome, _reference_bases, _alternate_bases, _reference_genome, _dataset_ids,
		_limit, _offset, _filters, _filters_converted, _join_variant_table;
	
	-- Aliases used in ontology_term_table
	-- 	'pat'
	-- 	'sam'
	-- 	'pat_ped'
	-- 	'pat_dis'
	-- In the future, we may have filters on beacon_data_table
	
	-- Check what other tables should be joined depending on the filters provided
	IF _filters_converted LIKE '%dat.%' THEN _join_variant_table=TRUE; END IF;
	
	RAISE NOTICE '_biosample_stable_id=%', _biosample_stable_id; 
	RAISE NOTICE '_individual_stable_id=%', _individual_stable_id;

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
		LEFT JOIN public.patient_pedigree_w_ontology_terms pat_ped ON pat_ped.patient_id=pat.id
		LEFT JOIN public.pedigree_table ped ON ped.id=pat_ped.pedigree_id
		LEFT JOIN public.patient_disease_w_ontology_terms pat_dis ON pat_dis.patient_id=pat.id 
		INNER JOIN public.beacon_sample_table sam ON sam.patient_id=pat.id
		INNER JOIN public.beacon_dataset_sample_table dataset_sam ON dataset_sam.sample_id=sam.id
		';
	
	
	-- Join other tables only if they are necessary
	IF _join_variant_table THEN
		_query = _query || '
		INNER JOIN public.beacon_data_sample_table dat_sam ON dat_sam.sample_id=sam.id
		INNER JOIN public.beacon_data_table bdat ON bdat.id=dat_sam.data_id
		INNER JOIN public.beacon_dataset_table bdataset ON bdataset.id=bdat.dataset_id
		';
	END IF;
	
	
	-- Datasets
	_query = _query || '
		WHERE dataset_sam.dataset_id = ANY (string_to_array($7, '','')::int[])';
	

	IF _biosample_stable_id IS NOT NULL THEN
		_query =  _query || '
		AND sam.stable_id=$13';
	END IF;
	

	IF _individual_stable_id IS NOT NULL THEN
		_query =  _query || '
		AND pat.stable_id=$14';
	END IF;
	

	IF _filters IS NOT NULL THEN
		_query = _query || ' 
		AND ' ||
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
			_query = _query || '
			AND bdat.type=$1 AND';
		END IF;

		raise notice '_alternate_bases: %', _alternate_bases;
		raise notice '_dataset_ids: %', _dataset_ids;

		IF _start_min IS NOT NULL THEN
			_query = _query || '
			AND bdat.start >= $9 AND bdat.start < $10
			AND bdat.end >= $11	AND bdat.end < $12';
		ELSIF _alternate_bases != '*' OR (_alternate_bases = '*' AND _end IS NULL)
			OR (_alternate_bases IS NULL AND _variant_type IS NOT NULL) THEN
		  -- Looking for an exact match
			_query = _query || '
			AND bdat.start = $2';
		END IF;


		IF _end IS NOT NULL THEN
			-- Remember that end is exclusive
			IF _alternate_bases = '*' THEN
				-- Looking for any variant within this range
				_query = _query || '
				AND (bdat.start >= $2 AND bdat.start < $8
				OR bdat.end >= $2 AND bdat.end < $8)';
			ELSE
				-- Looking for an exact match
				_query = _query || '
				AND bdat.end = ($8-1)';
			END IF;
		END IF;

		-- Chromosome
		_query = _query || '
		AND bdat.chromosome=$3';

		-- Reference parameter is not mandatory
		IF _reference_bases IS NOT NULL AND _reference_bases!='N' THEN
			_query=_query || '
			AND bdat.reference=$4';
		END IF;

		-- Alternate bases
		IF _alternate_bases IS NOT NULL THEN
		  IF _variant_type='INS' THEN
			  _query = _query || '
			  AND bdat.alternate like bdat.reference || $5 || ''%'' ';
			ELSIF _alternate_bases NOT IN ('N','*') THEN
			  _query = _query || '
			  AND bdat.alternate=$5';
			END IF;
		END IF;

		-- Convert reference_genome column to lower case
		_query = _query || '
		AND lower(bdataset.reference_genome)=$6';
	END IF;


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
		_reference_genome, _dataset_ids, _end, _start_min, _start_max, _end_min, _end_max, 
		_biosample_stable_id, _individual_stable_id, _limit, _offset;
	-- #1=_variant_type, #2=_start, #3=_chromosome, #4=_reference_bases, #5=_alternate_bases, 
	-- #6=_reference_genome, #7=_dataset_ids, #8=_end, #9=_start_min, #10=_start_max, 
	-- #11=_end_min, #12=_end_max, #13=_biosample_stable_id, #14=_individual_stable_id,
	-- #15=_limit, #16=_offset
END
$BODY$;