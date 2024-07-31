.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: docker-start
docker-start:	## Start server
	docker-compose build
	docker-compose up

.PHONY: test
test:	## Start tests
	docker exec jetiaspan_web python3 manage.py test

.PHONY: env
env:	## Install Dependencies
	python3 -m venv venv
	source venv/bin/activate

.PHONY: requirements
requirements:	## Install Dependencies
	pip3 install -r requirements.txt

.PHONY: run
run:	## Install Dependencies
	python3 manage.py runserver 8000
