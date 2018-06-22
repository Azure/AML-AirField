URL=${1:-127.0.0.1:9090/score}
AUTH=${2:+"Authorization: Bearer $2"}
IN_FILE=${3:-../SampleImages/dog.jpg}
OUT_FILE=${4:-out.png}

curl $URL -H "$AUTH" --data-binary @$IN_FILE
echo ""

rm $OUT_FILE
curl $URL?output=image -s -H "$AUTH" --data-binary @$IN_FILE --output $OUT_FILE
xdg-open $OUT_FILE
