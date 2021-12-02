
from dataclasses import dataclass
from strenum import StrEnum

@dataclass
class DefaultSchemas(StrEnum):
    ANALYSES = "beacon-analysis-v2.0.0-draft.4"
    BIOSAMPLES = "beacon-dataset-v2.0.0-draft.4"
    COHORTS = "beacon-cohort-v2.0.0-draft.4"
    DATASETS = "beacon-dataset-v2.0.0-draft.4"
    GENOMICVARIATIONS = "beacon-g_variant-v2.0.0-draft.4"
    INDIVIDUALS = "beacon-individual-v2.0.0-draft.4"
    RUNS = "beacon-run-v2.0.0-draft.4"
