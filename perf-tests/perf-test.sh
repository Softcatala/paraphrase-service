if [ -z "$1" ]
then
    URL="http://localhost:8000/paraphrase"
else
    URL=$1
fi

echo "Doing test on URL:" $URL

TIMEOUT=10s
CLIENTS=2
TEST_TIME=30s
wrk -t1 -T$TIMEOUT -c$CLIENTS -d $TEST_TIME -s post-paraphrase.form.lua $URL


