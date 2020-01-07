#!/usr/bin/env bats

load helpers

@test "Query [GRCh37] Y: 2655179 G > A (ALL)" {

    query="${BEACON_URL}/query?referenceName=Y&start=2655179&assemblyId=GRCh37&referenceBases=G&alternateBases=A&includeDatasetResponses=ALL"
    response="query.json"

    run diff -y \
	<(curl "${query}" 2>/dev/null | jq -S '.') \
	<(get_response $response)
    [[ "$status" = 0 ]]

}
