from aiohttp import web

from beacon.db import analyses, biosamples, cohorts, datasets, g_variants, individuals, runs, filtering_terms
from beacon.request.handlers import collection_handler, generic_handler, filtering_terms_handler
from beacon.response import framework, info, service_info, error

routes = [

    ########################################
    # CONFIG
    ########################################

    web.get('/api', info.handler),
    web.get('/api/info', info.handler, name="info"),    # Name added to redirect / -> /info
    web.get('/api/service-info', service_info.handler),
    web.get('/api/filtering_terms', filtering_terms_handler(db_fn=filtering_terms.get_filtering_terms)),

    web.get('/api/configuration', framework.configuration),
    web.get('/api/entry_types', framework.entry_types),
    web.get('/api/map', framework.beacon_map),

    ########################################
    # GET
    ########################################

    web.get('/api/analyses', generic_handler(db_fn=analyses.get_analyses)),
    web.get('/api/analyses/filtering_terms', filtering_terms_handler(db_fn=analyses.get_filtering_terms_of_analyse)),
    web.get('/api/analyses/{id}', generic_handler(db_fn=analyses.get_analysis_with_id)),
    web.get('/api/analyses/{id}/g_variants', generic_handler(db_fn=analyses.get_variants_of_analysis)),

    web.get('/api/biosamples', generic_handler(db_fn=biosamples.get_biosamples)),
    web.get('/api/biosamples/filtering_terms', filtering_terms_handler(db_fn=biosamples.get_filtering_terms_of_biosample)),
    web.get('/api/biosamples/{id}', generic_handler(db_fn=biosamples.get_biosample_with_id)),
    web.get('/api/biosamples/{id}/g_variants', generic_handler(db_fn=biosamples.get_variants_of_biosample)),
    web.get('/api/biosamples/{id}/analyses', generic_handler(db_fn=biosamples.get_analyses_of_biosample)),
    web.get('/api/biosamples/{id}/runs', generic_handler(db_fn=biosamples.get_runs_of_biosample)),

    web.get('/api/cohorts', collection_handler(db_fn=cohorts.get_cohorts)),
    web.get('/api/cohorts/filtering_terms', filtering_terms_handler(db_fn=cohorts.get_filtering_terms_of_cohort)),
    web.get('/api/cohorts/{id}', collection_handler(db_fn=cohorts.get_cohort_with_id)),
    web.get('/api/cohorts/{id}/individuals', generic_handler(db_fn=cohorts.get_individuals_of_cohort)),
    web.get('/api/cohorts/{id}/analyses', generic_handler(db_fn=cohorts.get_analyses_of_cohort)),
    web.get('/api/cohorts/{id}/biosamples', generic_handler(db_fn=cohorts.get_biosamples_of_cohort)),
    web.get('/api/cohorts/{id}/g_variants', generic_handler(db_fn=cohorts.get_variants_of_cohort)),
    web.get('/api/cohorts/{id}/runs', generic_handler(db_fn=cohorts.get_runs_of_cohort)),

    web.get('/api/datasets', collection_handler(db_fn=datasets.get_datasets)),
    web.get('/api/datasets/filtering_terms', filtering_terms_handler(db_fn=datasets.get_filtering_terms_of_dataset)),
    web.get('/api/datasets/{id}', collection_handler(db_fn=datasets.get_dataset_with_id)),
    web.get('/api/datasets/{id}/g_variants', generic_handler(db_fn=datasets.get_variants_of_dataset)),
    web.get('/api/datasets/{id}/biosamples', generic_handler(db_fn=datasets.get_biosamples_of_dataset)),
    web.get('/api/datasets/{id}/individuals', generic_handler(db_fn=datasets.get_individuals_of_dataset)),
    web.get('/api/datasets/{id}/runs', generic_handler(db_fn=datasets.get_runs_of_dataset)),
    web.get('/api/datasets/{id}/analyses', generic_handler(db_fn=datasets.get_analyses_of_dataset)),

    web.get('/api/g_variants', generic_handler(db_fn=g_variants.get_variants)),
    web.get('/api/g_variants/filtering_terms', filtering_terms_handler(db_fn=g_variants.get_filtering_terms_of_genomicvariation)),
    web.get('/api/g_variants/{id}', generic_handler(db_fn=g_variants.get_variant_with_id)),
    web.get('/api/g_variants/{id}/biosamples', generic_handler(db_fn=g_variants.get_biosamples_of_variant)),
    web.get('/api/g_variants/{id}/individuals', generic_handler(db_fn=g_variants.get_individuals_of_variant)),
    web.get('/api/g_variants/{id}/runs', generic_handler(db_fn=g_variants.get_runs_of_variant)),
    web.get('/api/g_variants/{id}/analyses', generic_handler(db_fn=g_variants.get_analyses_of_variant)),


    web.get('/api/individuals', generic_handler(db_fn=individuals.get_individuals)),
    web.get('/api/individuals/filtering_terms', filtering_terms_handler(db_fn=individuals.get_filtering_terms_of_individual)),
    web.get('/api/individuals/{id}', generic_handler(db_fn=individuals.get_individual_with_id)),
    web.get('/api/individuals/{id}/g_variants', generic_handler(db_fn=individuals.get_variants_of_individual)),
    web.get('/api/individuals/{id}/biosamples', generic_handler(db_fn=individuals.get_biosamples_of_individual)),
    web.get('/api/individuals/{id}/runs', generic_handler(db_fn=individuals.get_runs_of_individual)),
    web.get('/api/individuals/{id}/analyses', generic_handler(db_fn=individuals.get_analyses_of_individual)),

    web.get('/api/runs', generic_handler(db_fn=runs.get_runs)),
    web.get('/api/runs/filtering_terms', filtering_terms_handler(db_fn=runs.get_filtering_terms_of_run)),
    web.get('/api/runs/{id}', generic_handler(db_fn=runs.get_run_with_id)),
    web.get('/api/runs/{id}/g_variants', generic_handler(db_fn=runs.get_variants_of_run)),
    web.get('/api/runs/{id}/analyses', generic_handler(db_fn=runs.get_analyses_of_run)),

    web.get('/api/{tail:.*}', error.handler),
    web.get('/{tail:.*}', error.handler),



    ########################################
    # POST
    ########################################
    web.post('/api', info.handler),
    web.post('/api/analyses', generic_handler(db_fn=analyses.get_analyses)),
    web.post('/api/analyses/filtering_terms', filtering_terms_handler(db_fn=analyses.get_filtering_terms_of_analyse)),
    web.post('/api/analyses/{id}', generic_handler(db_fn=analyses.get_analysis_with_id)),
    web.post('/api/analyses/{id}/g_variants', generic_handler(db_fn=analyses.get_variants_of_analysis)),

    web.post('/api/biosamples', generic_handler(db_fn=biosamples.get_biosamples)),
    web.post('/api/biosamples/filtering_terms', filtering_terms_handler(db_fn=biosamples.get_filtering_terms_of_biosample)),
    web.post('/api/biosamples/{id}', generic_handler(db_fn=biosamples.get_biosample_with_id)),
    web.post('/api/biosamples/{id}/g_variants', generic_handler(db_fn=biosamples.get_variants_of_biosample)),
    web.post('/api/biosamples/{id}/analyses', generic_handler(db_fn=biosamples.get_analyses_of_biosample)),
    web.post('/api/biosamples/{id}/runs', generic_handler(db_fn=biosamples.get_runs_of_biosample)),

    web.post('/api/cohorts', collection_handler(db_fn=cohorts.get_cohorts)),
    web.post('/api/cohorts/filtering_terms', filtering_terms_handler(db_fn=cohorts.get_filtering_terms_of_cohort)),
    web.post('/api/cohorts/{id}', collection_handler(db_fn=cohorts.get_cohort_with_id)),
    web.post('/api/cohorts/{id}/individuals', generic_handler(db_fn=cohorts.get_individuals_of_cohort)),
    web.post('/api/cohorts/{id}/analyses', generic_handler(db_fn=cohorts.get_analyses_of_cohort)),
    web.post('/api/cohorts/{id}/biosamples', generic_handler(db_fn=cohorts.get_biosamples_of_cohort)),
    web.post('/api/cohorts/{id}/filtering_terms', generic_handler(db_fn=cohorts.get_filtering_terms_of_cohort)),
    web.post('/api/cohorts/{id}/g_variants', generic_handler(db_fn=cohorts.get_variants_of_cohort)),
    web.post('/api/cohorts/{id}/runs', generic_handler(db_fn=cohorts.get_runs_of_cohort)),

    web.post('/api/datasets', collection_handler(db_fn=datasets.get_datasets)),
    web.post('/api/datasets/filtering_terms', filtering_terms_handler(db_fn=datasets.get_filtering_terms_of_dataset)),
    web.post('/api/datasets/{id}', collection_handler(db_fn=datasets.get_dataset_with_id)),
    web.post('/api/datasets/{id}/g_variants', generic_handler(db_fn=datasets.get_variants_of_dataset)),
    web.post('/api/datasets/{id}/biosamples', generic_handler(db_fn=datasets.get_biosamples_of_dataset)),
    web.post('/api/datasets/{id}/individuals', generic_handler(db_fn=datasets.get_individuals_of_dataset)),
    web.post('/api/datasets/{id}/filtering_terms', filtering_terms_handler(db_fn=datasets.get_filtering_terms_of_dataset)),
    web.post('/api/datasets/{id}/runs', generic_handler(db_fn=datasets.get_runs_of_dataset)),
    web.post('/api/datasets/{id}/analyses', generic_handler(db_fn=datasets.get_analyses_of_dataset)),

    web.post('/api/g_variants', generic_handler(db_fn=g_variants.get_variants)),
    web.post('/api/g_variants/filtering_terms', filtering_terms_handler(db_fn=g_variants.get_filtering_terms_of_genomicvariation)),
    web.post('/api/g_variants/{id}', generic_handler(db_fn=g_variants.get_variant_with_id)),
    web.post('/api/g_variants/{id}/biosamples', generic_handler(db_fn=g_variants.get_biosamples_of_variant)),
    web.post('/api/g_variants/{id}/individuals', generic_handler(db_fn=g_variants.get_individuals_of_variant)),
    web.post('/api/g_variants/{id}/runs', generic_handler(db_fn=g_variants.get_runs_of_variant)),
    web.post('/api/g_variants/{id}/analyses', generic_handler(db_fn=g_variants.get_analyses_of_variant)),

    web.post('/api/individuals', generic_handler(db_fn=individuals.get_individuals)),
    web.post('/api/individuals/filtering_terms', filtering_terms_handler(db_fn=individuals.get_filtering_terms_of_individual)),
    web.post('/api/individuals/{id}', generic_handler(db_fn=individuals.get_individual_with_id)),
    web.post('/api/individuals/{id}/g_variants', generic_handler(db_fn=individuals.get_variants_of_individual)),
    web.post('/api/individuals/{id}/biosamples', generic_handler(db_fn=individuals.get_biosamples_of_individual)),
    web.post('/api/individuals/{id}/runs', generic_handler(db_fn=individuals.get_runs_of_individual)),
    web.post('/api/individuals/{id}/analyses', generic_handler(db_fn=individuals.get_analyses_of_individual)),

    web.post('/api/runs', generic_handler(db_fn=runs.get_runs)),
    web.post('/api/runs/filtering_terms', filtering_terms_handler(db_fn=runs.get_filtering_terms_of_run)),
    web.post('/api/runs/{id}', generic_handler(db_fn=runs.get_run_with_id)),
    web.post('/api/runs/{id}/g_variants', generic_handler(db_fn=runs.get_variants_of_run)),
    web.post('/api/runs/{id}/analyses', generic_handler(db_fn=runs.get_analyses_of_run)),

    web.post('/api/{tail:.*}', error.handler),
    web.post('/{tail:.*}', error.handler)

]
