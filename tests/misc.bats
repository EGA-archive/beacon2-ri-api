#!/usr/bin/env bats

load helpers

@test "Datasets" {

    query="${BEACON_URL}/api/datasets"
    response="datasets.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Filtering Terms" {

    query="${BEACON_URL}/api/filtering_terms"
    response="filtering_terms.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}
