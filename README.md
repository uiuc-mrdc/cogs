# CoGS Web Services

This repository contains resources for building and running "Containerized Game Services," the web services for the [Midwestern Robotics Design Competition](http://mrdc.ec.illinois.edu/).

For now, that's just [Django](https://www.djangoproject.com/) and [MongoDB](https://www.mongodb.com/) running in [Docker Compose](https://docs.docker.com/compose/) with [Djongo](https://nesdis.github.io/djongo/) as a connector.

## Prerequisites

- [Docker CE](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Useful Documentation

- [Docker Compose command-line reference](https://docs.docker.com/compose/reference/overview/)
- [Docker Compose YAML file reference](https://docs.docker.com/compose/compose-file/)

## Contact Information

The point of creating CoGS is to have a solution for the MRDC game server that is as portable, maintainable, and transparent as possible. We learned our lesson from [Dredd](https://github.com/uiuc-mrdc/game-server).

In case this documentation is insufficient, or there are other problems with this system, you can contact [lpulley](https://lpulley.me/).

## Detailed Documentation

### Running and Stopping

Run `docker-compose up -d` in the root of this repo to start all of the CoGS services in the background, or to update the containers if they are already running.

To stop the containers, run `docker-compose stop`. To restart them use `docker-compose start`. To stop the containers and delete them, use `docker-compose down` (note that while this does delete volumes, it does **not** delete host files, so for example the database data in `./data-db` will persist). The `down` subcommand is useful for starting from *almost* scratch, such that only data linked to the host filesystem persists, but every service is completely recycled.

To start with the database from scratch, remove `./data-db` after `docker-compose down`. When you start up again, the database will create a new `./data-db`. Note that if you do this, the database will be missing some vital default models from Django, so you must migrate the models to the database. In Django, this is done with `python manage.py migrate`. **However**, since Django is running inside the `web` service, you must use `docker-compose exec <service> <command>` or `docker exec <container> <command>`. In this case, that would be `docker-compose exec web python manage.py migrate`.

In general, to run commands in a given service, use `docker-compose exec <service> <command>`. This will probably be very useful to you.
