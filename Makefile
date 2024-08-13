stack=exnada/python:latest
args=--rm -v '${PWD}'/src/:/home/exnada/src/
dockerrun=docker run -it
dockerframe=${dockerrun} ${args} ${stack}
bash=/bin/bash

build:
	@docker build -t ${stack} docker --build-arg OWNER=exnada
	@echo -n "Built image size: "
	@docker images ${stack} --format "{{.Size}}"

remove-container:
	docker image rm -f ${stack}

force-build:
	@docker build --rm --force-rm -t ${stack} ./docker --build-arg OWNER=exnada
	@echo -n "Built image size: "
	@docker images ${stack} --format "{{.Size}}"

all: 
	${dockerframe} make -C /home/exnada/src/

%:
	${dockerframe} make -C /home/exnada/src/ $(MAKECMDGOALS)

bash:
	${dockerframe} ${bash}

bashroot:
	${dockerrun} --user root ${args} ${stack} ${bash}
