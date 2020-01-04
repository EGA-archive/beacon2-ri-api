#!/usr/bin/env bats

load helpers

@test "Info Basic" {

    query="${BEACON_URL}/"
    response="info.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.updateDateTime)') \
	<(get_response $response 'del(.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Info Basic 2" {

    query="${BEACON_URL}/info"
    response="info.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.updateDateTime)') \
	<(get_response $response 'del(.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Service info " {

    query="${BEACON_URL}/service-info"
    response="info-service.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'del(.updateDateTime)') \
	<(get_response $response 'del(.updateDateTime)')
    [[ "$status" = 0 ]]

}

@test "Services" {

    query="${BEACON_URL}/services"
    response="services.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response)
    [[ "$status" = 0 ]]

}
