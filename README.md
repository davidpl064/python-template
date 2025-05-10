# Python Template
[![CI](https://github.com/davidpl064/python-template/actions/workflows/ci.yml/badge.svg)](https://github.com/davidpl064/python-template/actions/workflows/ci.yml)

This repository aims to serve as a Python project template, providing all necessary framework (management tool, Github workflows, structure), simplifying creation of new repositories.

## Project management tool
There are two main project management tools which can be used depending on project's requirements in terms of used programming languages and needed external dependencies, namely `uv` and `pixi`.

For Python-only projects, the selected tool to manage projects and perform operations like dependency management, building-packaging and environment handling is `uv`. The main CLI commands using `uv`are going to be detailed below, for further description of this tool and its main characteristics check its [Official Page](https://docs.astral.sh/uv/):

```
# Synchronize dependencies in `pyproject.toml` file with installed ones
uv sync

# Activation/deactivation of created environment (.venv directory in project's root directory)
. ./.venv/bin/activate
deactivate

# Add/remove new dependency
uv add package_name
uv remove package_name

# Specific version
uv add "httpx>=0.20"

# Custom package source
uv add "httpx @ git+https://github.com/encode/httpx"

# Add from file
uv add -r requirements.txt

# Add dependency to certain group (like `dev` or `test`)
uv add "httpx>=0.20" --dev

# Lock dependencies on `uv.lock` file and sync with `pyproject.toml`
# Check dependencies sync
uv lock --check

# Sync dependencies
uv lock

# Building the module and packaging
uv build

# Output artifacts are written to a folder in project's root directory called `/dist`. To publish the generated artifacts to cloud storage like PyPi
uv publish

# To set a destination other than PyPi, change the `pyproject.toml` file adding a section
[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
publish-url = "https://test.pypi.org/legacy/"

# Use the command, with the name set on the project file
uv publish --index <name>
```

## Project management tool: alternative multi-language support
To support cases where it is needed to use dependencies in other languages apart from Python, the alternative is the aforementioned `pixi`. This tool uses `uv` in the background for Python dependencies, and implements Conda-like interface for dependencies in other languages. Moreover, `pixi` allows to define environments with indendent dependencies (useful in cases where development is done in different hardware solutions). The main CLI commands using `pixi`are going to be detailed below, for further description of this tool and its main characteristics check its [Official Page](https://prefix.dev/):

```
# Synchronize dependencies in `pyproject.toml` file with installed ones
pixi shell

# Activation/deactivation of created environment (.pixi directory in project's root directory)
pixi shell
exit

# Activate spceific environment (env called "my-env")
pixi shell -e my-env

# Add/remove non PyPI dependency
pixi add package_name
pixi remove package_name

# Add/remove PyPI dependency
pixi add package_name --pypi
pixi remove package_name

# Specific version
pixi add "httpx>=0.20"

# Custom package source
pixi add "httpx @ git+https://github.com/encode/httpx"

# Add from file
pixi add -r requirements.txt

# Add dependency to certain group (like `dev` or `test`)
pixi add "httpx>=0.20" --dev

Lock dependencies on `pixi.lock` file and sync with `pyproject.toml`
pixi lock

# Building the module and packaging
pixi build

# List packages in activated environment
pixi list
```

---

# PythonModule
Short intro to the project (objective, scope, etc).

## Installation
It is needed to install the corresponding project management tool alongside some additional tools prior to start working in the project. To install the project management tool:
- [uv official website](https://docs.astral.sh/uv/getting-started/installation/):
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
- [pixi official website](https://prefix.dev/):
    ```
    curl -fsSL https://pixi.sh/install.sh | bash
    ```

It is also needed to install `make`, which will be used to run commands:
```
sudo apt update
sudo apt install make
```

## Makefile
To simplify all the operations needed to manage a project, and provide a natural and tool-agnostic interface, `make` commands are used. This way, whichever management tool is used (`uv` or other), the CLI commands would remain the same:
```
# Install dependencies
make install ## production dependencies
make install-dev ## development dependencies
make install-test ## test dependencies

# Build package
make build

# Linting
make lint

# Test
make test
make test-cov ## with coverage report

# Run module
make run

# Help
make help
```

## Commits Convention
It is encouraged to follow some conventions when defining commit messages, so it is easier and quicker for everyone to understand the purpose/scope of some changes, and also helps automating workflow processes. The documentation of current convention can be checked in [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

## Packages Custom Indexes
To download packages from custom indexes with authentication requirements, it is needed to provide the credentials, which is done in different ways depending on the actual index. This is a work in progress feature that would be improved. The process to authenticate to `Nexus` index `requires` to provide user and password, which are provided through environment variables. `uv` currently can't directly read all environment variables, so to be able to access them, they must follow some name pattern:
- username: "UV_INDEX_NEXUS_USERNAME"
- password: "UV_INDEX_NEXUS_PASSWORD"

To use secrets in docker build commands, it is encouraged to use docker secrets feature during build process. The build command reads from local environment variables like aforementioned.

It is `mandatory` to save our credentials under those names.
