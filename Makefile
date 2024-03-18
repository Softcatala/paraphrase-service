build-all: docker-build

docker-build:
	docker build --no-cache -t paraphrase-service . -f docker/dockerfile;
	docker image ls | grep 	paraphrase-service

docker-run:
	docker run -it --rm -p 8000:8000 paraphrase-service;

download_models:
	git clone --depth=1 https://gitlab.softcatala.org/jmas/paraphrase-service-model /srv/model
