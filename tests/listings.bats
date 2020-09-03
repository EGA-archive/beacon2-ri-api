#!/usr/bin/env bats

load helpers

@test "Biosamples" {

    query="${BEACON_URL}/api/biosamples"
    response="biosamples.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Biosamples - SAMEA4806673" {

    query="${BEACON_URL}/api/biosamples/SAMEA4806673"
    response="biosamples-1.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Biosamples - SAMEA4806673 - individuals" {

    query="${BEACON_URL}/api/biosamples/SAMEA4806673/individuals"
    response="biosamples-2.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Biosamples - SAMEA4806673 - g_variants" {

    query="${BEACON_URL}/api/biosamples/SAMEA4806673/g_variants"
    response="biosamples-3.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Individuals" {

    query="${BEACON_URL}/api/individuals"
    response="individuals.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Individuals - NA24631" {

    query="${BEACON_URL}/api/individuals/NA24631"
    response="individuals-1.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Individuals - NA24631 - biosamples" {

    query="${BEACON_URL}/api/individuals/NA24631/biosamples"
    response="individuals-2.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Individuals - NA24631 - g_variants" {

    query="${BEACON_URL}/api/biosamples/SAMEA4806673/g_variants"
    response="individuals-3.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "GVariants" {

    query="${BEACON_URL}/api/g_variants"
    response="gvariants.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "GVariants - 1" {

    query="${BEACON_URL}/api/g_variants/1"
    response="gvariants-1.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "GVariants - 1 - biosamples" {

    query="${BEACON_URL}/api/g_variants/1/biosamples"
    response="gvariants-2.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "GVariants - 1 - individuals" {

    query="${BEACON_URL}/api/g_variants/1/individuals"
    response="gvariants-3.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}
