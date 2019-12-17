"""
This file contains the dictionaries that link the objects of the responses of the main endpoints to
the name they have in the access levels file, so they can be compared in the filtering step.
"""

info2access = {
    "organization": "beaconOrganization",
    "datasets": "beaconDataset"
}

query2access = {
    "datasetAlleleResponses": "datasetAlleleResponse",
    "alleleRequest": "beaconAlleleRequest"
}

snp2access = {
    "datasetAlleleResponses": "datasetAlleleResponse",
    "request": "beaconGenomicSnpRequest"
}

region2access = {
    "variantsFound": "variant",
    "datasetAlleleResponses": "datasetAlleleResponse",
    "request": "beaconGenomicRegionRequest"
}