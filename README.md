# CoGS Web Services

This repository contains resources for building and running the web services for CoGS.

For now, that's just Django and MongoDB running in Docker Compose with Djongo as a connector.

## Prerequisites

- [Docker CE](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running and Stopping

Run `docker-compose up -d` in the root of this repo to start all of the CoGS services.

To stop the services, run `docker-compose stop`. To restart them use `docker-compose start`. To stop the services and delete the containers, use `docker-compose down` (note that while this does delete volumes, it does **not** delete host files, so for example the database data in `./data-db` will persist). The `down` subcommand is useful for starting from *almost* scratch, such that only data linked to the host filesystem persists, but every service is completely recycled.
