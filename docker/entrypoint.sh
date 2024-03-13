#/bin/sh
cd srv/web/
gunicorn  --workers=1 --graceful-timeout 90 --timeout 90 --threads=8 paraphrase-service:app -b 0.0.0.0:8000
