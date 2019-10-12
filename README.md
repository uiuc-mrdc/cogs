# CoGS Web Services

This repository contains resources for building and running the web services for CoGS.

For now, that's just Django and MongoDB running in Docker Compose with Djongo as a connector.

## Prerequisites

- [Docker CE](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running and Stopping

Run `docker-compose up -d` in the root of this repo to start all of the CoGS services.

To stop the services, run `docker-compose stop`. To restart them use `docker-compose start`. To stop the services and delete the containers, use `docker-compose down` (note that this does **not** delete volumes, so for example, the database data in `./data-db` will persist). The `down` subcommand is useful for starting from *almost* scratch, such that only important data persists, but every service is completely recycled.

If you do want to completely start from scratch, including rebuilding the Django image and deleting the volumes, you can try `docker system prune` once Docker Compose is `down`. This will delete all volumes, images, etc. that are not connected to a container.