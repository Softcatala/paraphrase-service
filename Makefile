build-all: docker-build

docker-build:
	docker build -t paraphrase-service . -f docker/dockerfile;
	docker image ls | grep 	paraphrase-service

docker-run: docker-build
	docker run -it --rm -p 8000:8000 paraphrase-service;

download_models:
	wget -O ct2.zip https://gitlab.softcatala.org/nous-projectes/paraphrase-training/-/package_files/89/download
	mkdir -p /srv/model/ && unzip ct2.zip -d /srv/model/
