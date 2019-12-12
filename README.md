# Forest Preserve of Cook County Document Search

Search and management interface for spatial documents, built for the Forest Preserve of Cook County.

## Developing

Development requires a local installation of [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

Build containers:

```
docker-compose build
```

Run the app:

```
docker-compose up
```

The app will be available at http://localhost:8000. The database will be exposed
on port 32001.

Create a superuser to view the application:

```
docker-compose run --rm app ./manage.py createsuperuser
```

Load initial data:

```
docker-compose run --rm app make all
```

### Running tests

Run tests with Docker Compose:

```
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```
