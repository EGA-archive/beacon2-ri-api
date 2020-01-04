#!/usr/bin/env bats

load helpers

@test "Access Levels Basic" {

    query="${BEACON_URL}/access_levels"
    response="access_levels-basic.json"

    run diff \
	<(curl "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response)
    [[ "$status" = 0 ]]

}

@test "Access Levels 'includeFieldDetails=true'" {

    query="${BEACON_URL}/access_levels?includeFieldDetails=true"
    response="access_levels-field_details.json"

    run diff \
	<(curl "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response)
    [[ "$status" = 0 ]]

}

@test "Access Levels 'displayDatasetDifferences=true'" {

    query="${BEACON_URL}/access_levels?displayDatasetDifferences=true"
    response="access_levels-dataset_diff.json"

    run diff \
	<(curl "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response)
    [[ "$status" = 0 ]]

}

@test "Access Levels 'displayDatasetDifferences=true&includeFieldDetails=true'" {

    query="${BEACON_URL}/access_levels?displayDatasetDifferences=true&includeFieldDetails=true"
    response="access_levels-det_and_diff.json"

    run diff \
	<(curl "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response)
    [[ "$status" = 0 ]]

}
