.PHONY: clean build run stop inspect

IMAGE_NAME = jekylmygi
CONTAINER_NAME = container_jekylmygithub
ABSOLUTE_PATH = /home/tigerit/MyGithub/shihabyasin.github.io_preprocess/tutorial-auto-upload/offline_jekyll_site_testing

build:   # 1. BUILD DOCKER IMAGE
	docker build -t $(IMAGE_NAME) .

run:     # 2. RUN DOCKER CONTAINER
	#docker run -d --rm -p 4000:4000 --name $(CONTAINER_NAME) $(IMAGE_NAME)
	docker run --rm -p 4000:4000 -v ${ABSOLUTE_PATH}/_posts:/home/user/my-awesome-site/_posts -v ${ABSOLUTE_PATH}/_includes:/home/user/my-awesome-site/_includes  -v ${ABSOLUTE_PATH}/_layouts:/home/user/my-awesome-site/_layouts -v ${ABSOLUTE_PATH}/public:/home/user/my-awesome-site/public -v ${ABSOLUTE_PATH}/_sass:/home/user/my-awesome-site/_sass  -v ${ABSOLUTE_PATH}/assets:/home/user/my-awesome-site/assets  --name $(CONTAINER_NAME) $(IMAGE_NAME)


stop:    # 3. STOP DOCKER CONTAINER
	docker stop $(CONTAINER_NAME)

list:    # 4. GET LIST OF DOCKER IMAGES & CONTAINERS
	# list all docker image and container
	docker image ls && docker container ls

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash


