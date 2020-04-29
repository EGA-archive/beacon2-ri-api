
CREATE OR REPLACE FUNCTION public.manage_datasets(
	IN _include_dataset_responses text,
	OUT _query text)
    LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
	_only_hit_datasets bool;
	_only_miss_datasets bool;
BEGIN
	_only_hit_datasets = FALSE;
	_only_miss_datasets = FALSE;
	
	IF _include_dataset_responses IN ('HIT','NONE') THEN
		_only_hit_datasets = TRUE;
	END IF;
	IF _include_dataset_responses = 'MISS' THEN
		_only_miss_datasets = TRUE;
	END IF;
	
	_query = '
	FROM public.beacon_dataset_table bdataset 
	LEFT JOIN vars_found ON vars_found.dataset_stable_id=bdataset.stable_id';

	IF _only_hit_datasets THEN
		_query = _query || '
		WHERE vars_found.id IS NOT NULL';
	ELSIF _only_miss_datasets THEN
		_query = _query || '
		WHERE vars_found.id IS NULL';
	END IF;

END
$BODY$;
