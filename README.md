# CoGS Web Services

This repository contains resources for building and running "Containerized Game Services," the web services for the [Midwestern Robotics Design Competition](http://mrdc.ec.illinois.edu/).

For now, that's just [Django](https://www.djangoproject.com/), [MariaDB](https://mariadb.org/) and [Redis](https://redis.io/) running in [Docker Compose](https://docs.docker.com/compose/)

## Required Software

- [Docker CE](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Useful Documentation

- [Docker Compose command-line reference](https://docs.docker.com/compose/reference/overview/)
- [Docker Compose YAML file reference](https://docs.docker.com/compose/compose-file/)

## Contact Information

The point of creating CoGS is to have a solution for the MRDC game server that is as portable, maintainable, and transparent as possible. We learned our lesson; we want CoGS to last for years and to be accessible to people who weren't here when we wrote it.

In case this documentation is insufficient, or there are other problems with this system, you can contact [lpulley](https://github.com/lpulley/).

## Detailed Documentation

### Running and Stopping

#### Startup

Run `docker-compose up -d` in the root of this repo to build images for custom containers and start all of the CoGS containers in the background, or to update the containers if they are already running.

#### Database Initialization

The database for this project takes a bit of time to initialize from an empty volume (when cloning the repo for the first time, or after running `docker-compose down -v` or otherwise having an empty `cogs_db` volume). To allow the database to properly initialize, after running `docker-compose up -d` the first time, monitor the database logs with `docker-compose logs -f db` and when it finishes initializing, `docker-compose restart` to allow Django to reconnect.

#### Stopping

To stop the containers, run `docker-compose stop`. To restart them use `docker-compose start`. To stop the containers and delete them, use `docker-compose down`. Note that while this does delete volume connections, it does **not** delete host files created by volumes, so for example the database data in `./data-db` will persist; images from `Dockerfile`s will also need to be manually deleted if they are to be rebuilt.

The `down` subcommand is useful for starting from *almost* scratch, such that only data in volumes persists, but every container is completely recycled. Running `docker-compose up -d` will start them anew, but does not rebuild images from `Dockerfile`s if they still exist. To rebuild images from `Dockerfile`s use `docker-compose build` or start with `docker-compose up -d --build`. This will force a rebuild of images that are listed in `docker-compose.yml` with a `build:` directory.

To start the database from scratch, use `docker-compose down -v` (the `-v` flag will remove named volumes). When you start up again, the database will create a new volume. Note that if you do this, the database will be missing some vital default models from Django, so you must migrate the models to the database. In Django, this is done with `python manage.py migrate`. **However**, since Django is running inside the `web` service, you must use `docker-compose exec <service> <command>` or `docker exec <container> <command>`. In this case, that would be `docker-compose exec web python manage.py migrate`.

#### Commands Inside Containers

In general, to run commands in a given service, use `docker-compose exec <service> <command>`. This will probably be very useful to you.

### CoGS for Dummies

Run these commands to start CoGS (assuming you've installed Docker and Docker Compose and cloned this repository):

```
docker-compose up -d
sleep 1m                # Wait for database to initialize
docker-compose restart  # Let Django reconnect to the database
docker-compose exec web python manage.py migrate
```
