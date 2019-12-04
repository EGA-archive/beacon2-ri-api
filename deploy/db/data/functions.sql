-- FUNCTION: public.query_data_summary_response(text, integer, integer, integer, integer, integer, integer, character varying, text, text, text, text, text)
-- DROP FUNCTION public.query_data_summary_response(text, integer, integer, integer, integer, integer, integer, character varying, text, text, text, text, text);
CREATE OR REPLACE FUNCTION public.query_data_summary_response(
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
	_filters text)
    RETURNS TABLE(id text, dataset_id integer, variant_cnt bigint, call_cnt bigint, sample_cnt bigint, frequency numeric, num_variants integer) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
DECLARE
	_query text;
BEGIN
	-- Initialize String parameters
	IF _variant_type IS NOT NULL AND _variant_type = 'null' THEN _variant_type = null; END IF;
	IF _chromosome IS NOT NULL AND _chromosome = 'null' THEN _chromosome = null; END IF;
	IF _reference_bases IS NOT NULL AND _reference_bases = 'null' THEN _reference_bases = null; END IF;
	IF _alternate_bases IS NOT NULL AND _alternate_bases = 'null' THEN _alternate_bases = null; END IF;
	IF _reference_genome IS NOT NULL AND _reference_genome = 'null' THEN _reference_genome = null; END IF;
	IF _dataset_ids IS NOT NULL AND _dataset_ids = 'null' THEN _dataset_ids = null; END IF;
	IF _filters IS NOT NULL AND _filters = 'null' THEN _filters = null; END IF;
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
	-- Check that mandatory parameters are present
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
	ELSIF _end IS NULL AND _reference_bases='N' THEN RAISE EXCEPTION '_reference_bases cannot be N if _end is missing';
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
	  THEN RAISE EXCEPTION 'Either _variant_type or _alternate_bases is mandatory';
	END IF;
	IF _alternate_bases='N' THEN _alternate_bases='*'; END IF; -- Look for any variant
	_query = '
	SELECT
		CONCAT(q.dataset_id, q.variant_cnt, q.call_cnt, q.sample_cnt, q.frequency, q.num_variants) AS id,
		q.dataset_id,
		q.variant_cnt,
		q.call_cnt,
		q.sample_cnt,
		q.frequency,
		q.num_variants
	';
	_query = _query || 'FROM (';
	_query = _query || '
	SELECT
		variants.dataset_id,
		variants.variant_cnt,
		variants.call_cnt,
		variants.sample_cnt,
		CASE WHEN variants.num_variants > 1
			THEN (variants.variant_cnt::decimal/variants.call_cnt)::decimal(10,10)
			ELSE variants.frequency END AS frequency,
		variants.num_variants
	FROM (
		SELECT bdat.dataset_id,
			max(bdat.variant_cnt)::bigint AS variant_cnt,
			max(bdat.call_cnt)::bigint AS call_cnt,
			--CASE WHEN count(*) > 1
			--	THEN coalesce,MAX(matching_samples.sample_cnt)::bigint
			--	ELSE max(bdat.matching_sample_cnt)::bigint END AS sample_cnt,
			max(bdat.sample_cnt)::bigint AS sample_cnt,
			max(bdat.frequency) AS frequency,
			COUNT(DISTINCT bdat.id)::integer AS num_variants
		FROM public.beacon_data_table bdat
		INNER JOIN public.beacon_dataset_table bdataset ON bdataset.id=bdat.dataset_id
		LEFT JOIN LATERAL (
			SELECT COALESCE(COUNT(DISTINCT bsam.sample_id), 0)::integer AS sample_cnt
			FROM public.beacon_data_sample_table bsam
			WHERE bsam.data_id=bdat.id
		) matching_samples ON TRUE
		WHERE';
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
	-- Datasets
	_query = _query || ' bdat.dataset_id = ANY (string_to_array($7, '','')::int[])';
	IF _filters IS NOT NULL THEN
		_query = _query || ' AND ' || _filters;
	END IF;
	_query = _query || '
			 --GROUP BY bdat.dataset_id
			  GROUP BY CONCAT(bdat.dataset_id, bdat.chromosome, bdat.variant_id, bdat.reference, bdat.alternate, bdat.start, bdat.end, bdat.type),
				bdat.chromosome, bdat.variant_id, bdat.reference, bdat.alternate, bdat.start, bdat.end, bdat.type, bdat.dataset_id
		) variants
		ORDER BY variants.dataset_id
	)q';
	RAISE NOTICE '_query: %', _query;
	RETURN QUERY EXECUTE _query
	USING _variant_type, _start, _chromosome, _reference_bases, _alternate_bases, _reference_genome, _dataset_ids, _end, _start_min, _start_max, _end_min, _end_max;
	-- #1=_variant_type, #2=_start, #3=_chromosome, #4=_reference_bases, #5=_alternate_bases, #6=_reference_genome, #7=_dataset_ids,
	-- #8=_end, #9=_start_min, #10=_start_max, #11=_end_min, #12=_end_max
END
$BODY$;