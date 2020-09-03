#!/usr/bin/env bats

load helpers

@test "Permissions - GVariants - Anonymous" {

    query="${BEACON_URL}/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21"
    response="gvariants-anonymous.json"
    #  unauthenticated user: 2 rows

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response '.')
    [[ "$status" = 0 ]]

}

@test "Permissions - GVariants - John" {

    query="${BEACON_URL}/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21"
    response="gvariants-john.json"
    # john: 8 rows

    TOKEN=$(get_token john john)
    [[ -n "$TOKEN" ]]

    run diff -y \
	<(curl -H "Authorization: ${TOKEN}" "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response '.')
    [[ "$status" = 0 ]]

}

@test "Permissions - GVariants - Jane" {

    query="${BEACON_URL}/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21"
    response="gvariants-jane.json"
    #  jane: 4 rows

    TOKEN=$(get_token jane jane)
    [[ -n "$TOKEN" ]]

    run diff -y \
	<(curl -H "Authorization: ${TOKEN}" "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response '.')
    [[ "$status" = 0 ]]

}

@test "Filter by registered dataset - Anonymous" {

    query="${BEACON_URL}/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21&datasetIds=dataset-registered"
    response="datasets-registered-anonymous.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response '.')
    [[ "$status" = 0 ]]

}

@test "Filter by registered dataset - John" {

    query="${BEACON_URL}/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21&datasetIds=dataset-registered"
    response="datasets-registered-john.json"

    TOKEN=$(get_token john john)
    [[ -n "$TOKEN" ]]

    run diff -y \
	<(curl -H "Authorization: ${TOKEN}" "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response '.')
    [[ "$status" = 0 ]]

}

@test "Filter by registered dataset - Jane" {

    query="${BEACON_URL}/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21&datasetIds=dataset-registered"
    response="datasets-registered-jane.json"

    TOKEN=$(get_token jane jane)
    [[ -n "$TOKEN" ]]

    run diff -y \
	<(curl -H "Authorization: ${TOKEN}" "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response '.')
    [[ "$status" = 0 ]]

}
