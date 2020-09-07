#!/usr/bin/env bats

load helpers

@test "Info" {

    query="${BEACON_URL}/api"
    response="info.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

    query="${BEACON_URL}/api/info"
    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Info - Schema" {

    query="${BEACON_URL}/api/info?requestedSchemasServiceInfo=ga4gh-service-info-v1.0"
    response="info_schema.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Service info" {

    query="${BEACON_URL}/api/service-info"
    response="service_info.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Info - Model" {

    query="${BEACON_URL}/api/info?model=ga4gh-service-info-v1.0"
    response="info_model.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.response.results.updateDateTime)') \
	<(get_response $response 'del(.response.results.updateDateTime)')
    [[ "$status" = 0 ]]

}
