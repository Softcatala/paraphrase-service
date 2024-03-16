build-all: docker-build

docker-build:
	docker build -t paraphrase-service . -f docker/dockerfile;
	docker image ls | grep 	paraphrase-service

docker-run:
	docker run -it --rm -p 8000:8000 paraphrase-service;

download_models_req:
	pip3 install -r requirements-modelconv.txt
	
MODEL_DIR=outputs.exp303.ct2

download_models:
	git clone --depth=1 https://gitlab.softcatala.org/jmas/paraphrase-models.git models.pt/ && cd models.pt/ && git lfs pull
	mkdir -p models/${MODEL_DIR}    
	cp models.pt/${MODEL_DIR}/* models/${MODEL_DIR}

