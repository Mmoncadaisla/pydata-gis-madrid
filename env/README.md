# Soy crop research Environment

## What's in this environment

The environment contains the following main features,

- PostgreSQL 12

- PostGIS 3

- Python 3.9

- Jupyter 

- Python geospatial packages: GeoPandas, GeoPy, rasterio, psycopg2

## Why this setup?

This setup has been chosen for the following main reasons,

- Geospatial manipulations
- Out of memory capacity
- Familiarity
- Open Source stack

This test has been run using a 16 GB RAM 8 core laptop with only OS software and no economical cost.

Looking for future developments, which could involve performing potentially out of memory operations or geospatial processes has pushed me to find what I believe was the right toolset for this purpose.

For this reason, I've chosen to use a combination of the following,

- Python, IMHO one of the most popular programming languages with a large variety of packages for analysis and tools for data analysis, application development and orchestration.

- PostgreSQL, an open source object-relational database system with over 30 years of active development according to the official docs

- PostGIS, a geospatial extension of the prior with support for a large amount of different geospatial operations.


## Set up with docker-compose :whale: :boom:

>NOTE: to install this environment both [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/) are required

1. Build with docker-compose build

```bash
docker-compose build
```

2. Start the corresponding containers with docker-compose up

```bash
docker-compose up
```

3. Access the link to access Jupyter within the notebooks directory 

To access the database through `psql` you could run the following,

* Open a new terminal in the postgres container

```bash
docker exec -it env_postgres_1 /bin/bash
```
* Access the database via psql

```bash
docker exec -it env_postgres_1 psql -U postgres -d research
```
