ADR=${1:-127.0.0.1:9090/score}
AUTH=${2:+"Authorization: Bearer $2"}
IN_FILE=${3:-./sample_input.json}

( set -x; curl $ADR -H "$AUTH" -H "Content-Type: application/json" -d @$IN_FILE )
echo ""