
CREATE OR REPLACE FUNCTION public.add_where_clause_conditions(
	IN _variant_type text,
	IN _start_min integer,
	IN _end integer,
	IN _reference_bases text,
	IN _alternate_bases text,
	IN _dataset_stable_ids text[],
	IN _is_authenticated bool,
	IN _biosample_stable_id text,
	IN _individual_stable_id text,
	IN _filters text,
	OUT _where_clause text)
    LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
	_join_variant_table bool;
BEGIN
	_where_clause = '
	WHERE ';
	_join_variant_table = FALSE;
	
	IF _variant_type IS NOT NULL OR _start_min IS NOT NULL OR _end IS NOT NULL 
		OR _reference_bases IS NOT NULL OR _alternate_bases IS NOT NULL
		THEN _join_variant_table = TRUE;
	END IF;

	-- Datasets
	IF NOT _is_authenticated OR _dataset_stable_ids IS NULL OR array_length(_dataset_stable_ids, 1) IS NULL THEN
		-- only query PUBLIC datasets
		_where_clause = _where_clause || '
		bdataset.access_type=''PUBLIC''';
	END IF;
	
	IF array_length(_dataset_stable_ids, 1) > 0 THEN
		IF NOT _is_authenticated THEN
			_where_clause =  _where_clause || '
			AND';
		END IF;
		_where_clause =  _where_clause || '
		bdataset.stable_id = ANY($7)';
	END IF;
		
	IF _biosample_stable_id IS NOT NULL THEN
		_where_clause =  _where_clause || '
		AND sam.stable_id=$13';
	END IF;
	
	IF _individual_stable_id IS NOT NULL THEN
		_where_clause =  _where_clause || '
		AND pat.stable_id=$14';
	END IF;
	
	IF _filters IS NOT NULL THEN
		_where_clause = _where_clause || ' 
		AND ' || _filters;
	END IF;

	IF _join_variant_table THEN
	
		IF _variant_type IS NULL AND _alternate_bases IS NULL
		  --THEN RAISE EXCEPTION 'Either _variant_type or _alternate_bases is mandatory';
		  THEN _alternate_bases='*';
		END IF;
		IF _alternate_bases='N' THEN _alternate_bases='*'; END IF; -- Look for any variant	
	
		IF _variant_type IS NOT NULL THEN
			_where_clause = _where_clause || '
			AND bdat.type=$1';
		END IF;

		IF _start_min IS NOT NULL THEN
			_where_clause = _where_clause || '
			AND bdat.start >= $9 AND bdat.start < $10
			AND bdat.end >= $11	AND bdat.end < $12';
		ELSIF _alternate_bases != '*' OR (_alternate_bases = '*' AND _end IS NULL)
			OR (_alternate_bases IS NULL AND _variant_type IS NOT NULL) THEN
		  	-- Looking for an exact match
			_where_clause = _where_clause || '
			AND bdat.start = $2';
		END IF;

		IF _end IS NOT NULL THEN
			-- Remember that end is exclusive
			IF _alternate_bases = '*' THEN
				-- Looking for any variant within this range
				_where_clause = _where_clause || '
				AND (bdat.start >= $2 AND bdat.start < $8
				OR bdat.end >= $2 AND bdat.end < $8)';
			ELSE
				-- Looking for an exact match
				_where_clause = _where_clause || '
				AND bdat.end = ($8-1)';
			END IF;
		END IF;

		-- Chromosome
		_where_clause = _where_clause || '
		AND bdat.chromosome=$3';

		-- Reference parameter is not mandatory
		IF _reference_bases IS NOT NULL AND _reference_bases!='N' THEN
			_where_clause=_where_clause || '
			AND bdat.reference=$4';
		END IF;

		-- Alternate bases
		IF _alternate_bases IS NOT NULL THEN
		  IF _variant_type='INS' THEN
			  _where_clause = _where_clause || '
			  AND bdat.alternate like bdat.reference || $5 || ''%'' ';
			ELSIF _alternate_bases NOT IN ('N','*') THEN
			  _where_clause = _where_clause || '
			  AND bdat.alternate=$5';
			END IF;
		END IF;

		-- Convert reference_genome column to lower case
		_where_clause = _where_clause || '
		AND lower(bdataset.reference_genome)=$6';
	END IF;

	-- #1=_variant_type, #2=_start, #3=_chromosome, #4=_reference_bases, #5=_alternate_bases, 
	-- #6=_reference_genome, #7=_dataset_stable_ids, #8=_end, #9=_start_min, #10=_start_max, 
	-- #11=_end_min, #12=_end_max, #13=_biosample_stable_id, #14=_individual_stable_id,
	-- #15=_limit, #16=_offset

END
$BODY$;
