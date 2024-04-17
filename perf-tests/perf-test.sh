if [ -z "$1" ]
then
    URL="http://localhost:8000/paraphrase"
else
    URL=$1
fi

echo "Doing test on URL:" $URL

wrk -t1 -c1 -d 10s -s post-paraphrase.form.lua $URL


