BEACON_URL=${BEACON_URL:-"http://beacon:5050"}

BEACON_CLIENT_ID=${BEACON_CLIENT_ID:-"beacon"}
BEACON_CLIENT_SECRET=${BEACON_CLIENT_SECRET:-"b26ca0f9-1137-4bee-b453-ee51eefbe7ba"}
IDP_TOKEN_URL=${IDP_TOKEN_URL:-"http://idp:8080/auth/realms/Beacon/protocol/openid-connect/token"}

function get_response {
    jq -S "${2:-.}" ${BATS_TEST_DIRNAME}/responses/$1
}

function get_token {
    curl -u "${BEACON_CLIENT_ID}:${BEACON_CLIENT_SECRET}" -X POST "${IDP_TOKEN_URL}" \
	 -d "grant_type=password&username=$1&password=$2" 2>/dev/null | jq -r ".access_token"
}
