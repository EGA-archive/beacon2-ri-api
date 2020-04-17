CREATE OR REPLACE FUNCTION public.parse_filters(
	IN _filters text[],
	OUT _filters_converted text)
    LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
	-- _filters format: array of CURIEs
	-- 		Example: ARRAY['NCIT:C46113','NCIT:C17600','GAZ:00001086']

	SELECT string_agg(q.my_filter, ' AND ') INTO _filters_converted
	FROM (
		select target_table_alias || '.' || column_name || '=' || quote_literal(column_value) as my_filter
		from (
			SELECT trim(split_part(filter_term,':',1)) AS ontology, 
				trim(split_part(filter_term,':',2)) AS term
			FROM unnest(_filters) AS filter_term
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

END
$BODY$;
