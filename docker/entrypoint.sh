#/bin/sh
cd srv/web/
# Need more workers than threads since it's a blocking request
gunicorn  --workers=4 --graceful-timeout 90 --timeout 90 --threads=1 paraphrase-service:app -b 0.0.0.0:8000
