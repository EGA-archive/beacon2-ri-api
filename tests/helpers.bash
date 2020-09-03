BEACON_URL=${BEACON_URL:-"http://beacon:5050"}

function get_response {
    jq -S "${2:-.}" ${BATS_TEST_DIRNAME}/responses/$1
}
