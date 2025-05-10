BASE_PROJECT_NAME := project-name
PROJECT_NAME := python-template
DOCKER_IMAGE_TAG := $(BASE_PROJECT_NAME)/$(PROJECT_NAME)
DOCKER_CONTAINER_NAME := $(BASE_PROJECT_NAME)-$(PROJECT_NAME)

GREEN_COLOR  := \033[0;32m
RESET_COLOR  := \033[0m

install: ## install package in "editable" mode
	uv sync
	@echo "Activate env with: $(GREEN_COLOR)source .venv/bin/activate$(RESET_COLOR)"
install-dev:  ## install package in "editable" mode with dev dependencies
	uv sync --dev
	uv run pre-commit install
	@echo "Activate env with: $(GREEN_COLOR)source .venv/bin/activate$(RESET_COLOR)"
install-test:  ## install package in "editable" mode with test dependencies
	uv sync --group test
	uv run pre-commit install
	@echo "Activate env with: $(GREEN_COLOR)source .venv/bin/activate$(RESET_COLOR)"

build:  ## build standalone package
	uv build

lint:  ## linting all files
	uv run pre-commit run --all-files

test:  ## run tests
	uv run pytest -svv ./tests
test-cov:  ## run tests with coverage reports (for Jenkins)
	uv run pytest --cov python_template \
		-o junit_family=xunit2 -o cache_dir=/tmp \
		--cov-report term-missing \
		--cov-report xml:./reports/coverage.xml --junitxml=./reports/junit-result.xml \
		-svv ./tests

run:  ## run on host
	uv run python -m python_template.main

docker-build: ## run docker build to create docker image
	docker build \
		--secret id=GIT_AUTH_TOKEN,env=GIT_TOKEN \
		--secret id=nexus-user,env=UV_INDEX_NEXUS_USERNAME \
		--secret id=nexus-pass,env=UV_INDEX_NEXUS_PASSWORD \
		-f docker/Dockerfile -t $(DOCKER_IMAGE_TAG) .

docker-run-dev: ## run docker image in dev mode (with network=host and using the local .env)
	docker run --rm --net=host --env-file .env --name $(DOCKER_CONTAINER_NAME) -t $(DOCKER_IMAGE_TAG) $(COMMAND)

docker-clean: ## remove docker image
	docker rmi $(DOCKER_IMAGE_TAG) || exit 0

help:  ## this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
