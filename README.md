# Forest Preserve of Cook County Document Search

Search and management interface for spatial documents, built for the Forest Preserve of Cook County.

## Developing

Development requires a local installation of [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

Before you start, you'll need a local settings file for development. If you're
on the Blackbox keyring for this repo, you can decrypt the canonical settings
file:

```
blackbox_cat configs/local_settings.dev.py.gpg > docsearch/local_settings.dev.py
```

Otherwise, copy and edit the example settings file:

```
cp docsearch/local_settings.example.py docsearch/local_settings.dev.py
```

Next, build containers:

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

To create the search index, start by bringing up Solr in one shell:

```
docker-compose up solr
```

Then, in another shell, run the `rebuild_index` command:

```
docker-compose run --rm app ./manage.py rebuild_index
```

### Running tests

Run tests with Docker Compose:

```
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```
