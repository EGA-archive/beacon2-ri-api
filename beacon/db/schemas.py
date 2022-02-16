from enum import Enum


class DefaultSchemas(Enum):
    ANALYSES = { "entityType": "analysis", "schema": "beacon-analysis-v2.0.0-draft.4" }
    BIOSAMPLES = { "entityType": "biosample", "schema": "beacon-dataset-v2.0.0-draft.4" }
    COHORTS = { "entityType": "cohort", "schema": "beacon-cohort-v2.0.0-draft.4" }
    DATASETS = { "entityType": "dataset", "schema": "beacon-dataset-v2.0.0-draft.4"}
    GENOMICVARIATIONS = { "entityType": "genomicVariation", "schema": "beacon-g_variant-v2.0.0-draft.4" }
    INDIVIDUALS = { "entityType": "individual", "schema": "beacon-individual-v2.0.0-draft.4" }
    RUNS = { "entityType": "run", "schema": "beacon-run-v2.0.0-draft.4" }
