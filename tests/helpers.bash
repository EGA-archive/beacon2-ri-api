[ ${BASH_VERSINFO[0]} -lt 4 ] && echo 'Bash 4 (or higher) is required' 1>&2 && exit 1

BEACON_DEBUG=${BEACON_DEBUG:-0}
BEACON_URL="http://localhost:5050" # no trailing /

# -----------------------------------
# Define the debug function
# -----------------------------------
if [[ "${BEACON_DEBUG}" -eq 0 ]]; then
    function debug { : ; }
else
    BEACON_DEBUG_FILE=${BEACON_DEBUG_FILE:-debug.output}
    function debug {
	echo "$@" >> ${BEACON_DEBUG_FILE}
    }
fi


# -----------------------------------
# Define the fetch_content function
# -----------------------------------
# See https://stackoverflow.com/a/24582523 about shell quoting
if [[ ${BEACON_DEBUG} == 1 ]]; then
    function fetch_content {
	local query=$1
	local pattern=${2:-.}
	debug "=================================================="
	debug "curl ${BEACON_URL}$query 2>/dev/null | jq -S $pattern"
	res=$(curl "${BEACON_URL}$query" 2>/dev/null | jq -S $pattern)
	local s=$?
	debug "==== Status: $?"
	debug "==== Output ===="
	debug "$res"
	echo -e "$res"
	return $((s))
    }
else
    function fetch_content {
	local query=$1
	local pattern=${2:-.}
	curl "${BEACON_URL}$query" 2>/dev/null | jq -S $pattern
    }
fi


# -----------------------------------
# Define the comparison function
# -----------------------------------
function compare {
    local query=$1
    local response=$2
    local pattern=${3:-.}

    # Formatting and Sorting keys with "jq -S"
    run diff -y <(fetch_content "$query" "$pattern") <(cat responses/${response} | jq -S .)

    if [[ "${BEACON_DEBUG}" -ne 0 ]] && [[ "$status" -ne 0 ]]; then
	debug "==== Diff output ===="
	debug "$output"
    fi
    echo $output
    return $status
}
