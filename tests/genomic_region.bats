#!/usr/bin/env bats

load helpers

@test "Genomic Region [GRCh37] Y: 2655179-2656125 (ALL)" {

    query="${BEACON_URL}/genomic_region?referenceName=Y&start=2655179&end=2656125&assemblyId=GRCh37&includeDatasetResponses=ALL"
    response="genomic_region-simple.json"

    run diff \
	<(curl "${query}" | jq -S 'walk(if type == "object" then del(.variantAnnotations) else . end)') \
	<(get_response $response 'walk(if type == "object" then del(.variantAnnotations) else . end)')
    [[ "$status" = 0 ]]

}
