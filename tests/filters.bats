#!/usr/bin/env bats

load helpers

@test "Filters - 1" {

    query="${BEACON_URL}/api/individuals?filters=NCIT:C27083,PATO:0000383" # no results
    response="filters-1.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Filters - 2" {

    query="${BEACON_URL}/api/individuals?filters=NCIT:C27083,PATO:0000384" # 1 result
    response="filters-2.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Filters - 3" {

    query="${BEACON_URL}/api/individuals?filters=PATO:0000384" # 2 results
    response="filters-3.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Filters - 4" {

    query="${BEACON_URL}/api/biosamples?filters=BTO:0000089" # 3 results
    response="filters-4.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Filters - 5" {

    query="${BEACON_URL}/api/biosamples?filters=BTO:0000089,NCIT:C37967" # 1 result
    response="filters-5.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}
