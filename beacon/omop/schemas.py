from enum import Enum


class DefaultSchemas(Enum):
    ANALYSES = {"entityType": "analysis", "schema": "beacon-analysis-v2.0.0"}
    BIOSAMPLES = {"entityType": "biosample", "schema": "beacon-dataset-v2.0.0"}
    COHORTS = {"entityType": "cohort", "schema": "beacon-cohort-v2.0.0"}
    DATASETS = {"entityType": "dataset", "schema": "beacon-dataset-v2.0.0"}
    FILTERINGTERMS = {"entityType": "filteringterms", "schema": "beacon-dataset-v2.0.0"}
    GENOMICVARIATIONS = {"entityType": "genomicVariation", "schema": "beacon-g_variant-v2.0.0"}
    INDIVIDUALS = {"entityType": "individual", "schema": "beacon-individual-v2.0.0"}
    RUNS = {"entityType": "run", "schema": "beacon-run-v2.0.0"}
