# fastapi-template
Basic FastAPI template. Defines a basic FastAPI app with postgres connecting with postgres


## Setup

need to add the following to your `~/.zshrc` to get this working with the correct user for migration file permissions:
```sh
export DOCKER_CURRENT_USER="$(id -u):$(id -g)"
```