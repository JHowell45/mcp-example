# fastapi-template
Basic FastAPI template. Defines a basic FastAPI app with postgres connecting with postgres


## Setup

_(This only seems to be an issue on my windows machine running on WSL2, you can ignore on a diff system or try first before adding the `DOCKER_CURRENT_USER` var)_
You will need to add the following to your `~/.zshrc` to get this working with the correct user for migration file permissions:
```sh
export DOCKER_CURRENT_USER="$(id -u):$(id -g)"
```

Running `docker-compose watch` should start all of the containers. One of the containers will handle the database migrations and importing the film data as ewll as vectorising the text. You can then visit the localhost for the example api and send vector queries to get text!