
load init

@test "POST - All individuals" {

    name="all-individuals"
    query="${BEACON_URL}/api/individuals/"
    request="requests/${name}.json"
    response="responses/${name}.json"

    echo "http POST $query --json < $request > ${BATS_TMPDIR}/${name}.json"
    http POST $query --json < $request | jq -S > "${BATS_TMPDIR}/${name}.json"
    run diff "${BATS_TMPDIR}/${name}.json" "${response}"

    [[ "$status" -eq 0 ]]
}

@test "POST - Individual NA24631" {

    name="individual-NA24631"
    query="${BEACON_URL}/api/individuals/NA24631/"
    request="requests/${name}.json"
    response="responses/${name}.json"

    echo "http POST $query --json < $request > ${BATS_TMPDIR}/${name}.json"
    http POST $query --json < $request | jq -S > "${BATS_TMPDIR}/${name}.json"
    run diff "${BATS_TMPDIR}/${name}.json" "${response}"

    [[ "$status" -eq 0 ]]
}


@test "Filters - Ontology Filter: Geographic Origin" {

    name="geographic-origin"
    query="${BEACON_URL}/api/individuals/"
    request="requests/${name}.json"
    response="responses/${name}.json"

    echo "http POST $query --json < $request > ${BATS_TMPDIR}/${name}.json"
    http POST $query --json < $request | jq -S > "${BATS_TMPDIR}/${name}.json"
    run diff "${BATS_TMPDIR}/${name}.json" "${response}"

    [[ "$status" -eq 0 ]]
}
