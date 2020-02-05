#!/usr/bin/env bats

load helpers

@test "Samples Filters + [GRCh37] Y: 2655179 G > A (ALL)" {

    query="${BEACON_URL}/samples?filters=sex:1,tissue:2&referenceName=Y&alternateBases=A&referenceBases=G&start=2655179&assemblyId=GRCh37"
    response="samples-filters_and_variant.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'walk(if type == "object" then del(.variantsFound) else . end)') \
	<(get_response $response 'walk(if type == "object" then del(.variantsFound) else . end)')
    [[ "$status" = 0 ]]

}

@test "Samples Filters" {

    query="${BEACON_URL}/samples?filters=sex:1,tissue:2"
    response="samples-filters.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S 'walk(if type == "object" then del(.variantsFound) else . end)') \
	<(get_response $response 'walk(if type == "object" then del(.variantsFound) else . end)')
    [[ "$status" = 0 ]]

}
