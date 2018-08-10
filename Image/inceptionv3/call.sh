ADR=${1:-127.0.0.1:9090/score}
AUTH=${2:+"Authorization: Bearer $2"}
IN_FILE=${3:-../SampleImages/dog.jpg}

( set -x; curl $ADR -H "$AUTH" --data-binary @$IN_FILE )
echo ""
echo ""

( set -x; curl $ADR?count=1 -H "$AUTH" --data-binary @$IN_FILE )
echo ""