# mcp-example
Example repo for showing the structure of how MCP should work

## References:
Dataset was pulled from here: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

# Setup:
This repo is orchestrated using docker compose. To start you will need to create a `.env` file that copies the values from the example, fill in any of the missing details with whatever username you like and passwords you prefer, anything that requires a specific command to be run will say so.


In order to start the service you need to run `docker-compose watch` this should pull the relevant images and start the services. There is a migration container that should run the db migrations so you can connect using your favorite db viewer and see how the data will be structured.

If you want to view the data jupyter labs has also been installed, you can run it by going into the `example-api` directory and running `uv run jupyter lab`. There is already a default notebook for viewing the data that's been imported.