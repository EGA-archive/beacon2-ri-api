#!/usr/bin/env bats

load helpers

@test "Variants SNP query" {

    query="${BEACON_URL}/api/g_variants?assemblyId=GRCh37.p1&referenceName=MT&referenceBases=T&alternateBases=C&start=150&includeDatasetResponses=ALL"
    response="snp-gvariants.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Biosamples by SNP" {

    query="${BEACON_URL}/api/biosamples?assemblyId=GRCh37.p1&referenceName=MT&referenceBases=T&alternateBases=C&start=150"
    response="snp-biosamples.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Individuals by SNP" {

    query="${BEACON_URL}/api/individuals?assemblyId=GRCh37.p1&referenceName=MT&referenceBases=T&alternateBases=C&start=150"
    response="snp-individuals.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Variants region query" {

    query="${BEACON_URL}/api/g_variants?assemblyId=GRCh37.p1&referenceName=MT&start=1&end=200"
    response="snp-region.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}
