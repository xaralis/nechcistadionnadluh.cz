# NechciStadionNaDluh.cz

A referendum presentation website.

It is built using Python on top of [Django](https://www.djangoproject.com/)
web framework and [PostgreSQL](https://www.postgresql.org/) database.

## Development

### Local installation

#### Prerequistes

This assumes you have **Python 3 installed**. To run in default
configuration, you also need **PostgreSQL server** up and running on `5432` port. You
also need a database and user ready. Defaults are:

* **Username**: `nsnd`
* **Database**: `nsnd`
* **Password**: `nsnd`

This can be changed by providing the `DATABASE_DSN` environment variable.

#### Installation

1. Clone the repository and cd into it

        git clone git@github.com:xaralis/nechcistadionnadluh.cz.git
        cd nechcistadionnadluh.cz

2. Initialize virtual environment and activate it

        make init-env
        source .env/bin/activate

3. Install dependencies

        make install-dev

4. Run the application

        make run

### Local installation using Docker

This app has docker-compose support prepared out-of-the-box. This will also
run PostgreSQL database in case you don't want to install it locally.

    docker-compose up

### Running tests

First, make sure you have test dependencies installed. Run:

    make install-test

From now on, you can run the test suite using:

    make test


## Configuration

All config is made using environment variables.

| Variable name  | Description                                                           | Required                | Default value                              |
|----------------|-----------------------------------------------------------------------|-------------------------|--------------------------------------------|
| `DEBUG`        | Turns on debug mode if equal to '1'. Shall not be used in production. | No                      | None                                       |
| `SECRET_KEY`   | Key used for encryption. Provide a long random string value.          | Yes if `DEBUG` is False | None                                       |
| `DATABASE_DSN` | Database connection string                                            | No                      | `postgresql://localhost:5432/nsnd` |


## Production deployment

This application is designed to be deployed as Docker container. Therefore,
you can use your preferred orchestration tool like [Kubernetes](https://kubernetes.io/)
or [Docker swarm](https://github.com/docker/swarm).

Or, you can simply launch it using Docker compose for small-scale installations
and/or testing purposes.

Docker images are continuosly pushed to the Docker Hub
[xaralis/nechcistadionnadluh.cz](https://hub.docker.com/r/xaralis/nechcistadionnadluh.cz/). App is
exposed via NginX proxy at port `80`.

1. Create your docker-compose.yml file somewhere:

    ```yaml
    version: '3.4'

    services:
        db:
            image: postgres:9.6.10-alpine
            volumes:
                - dbdata:/var/lib/postgresql
            restart: always
            ports:
                - "55433:5432"
            environment:
                POSTGRES_USER: nsnd
                POSTGRES_PASS: nsnd
                POSTGRES_DB: nsnd

        website:
            build:
                context: .
            volumes:
                - ./nsnd:/nsnd/nsnd
                - media:/media
                - thumbnails:/thumbnails
            ports:
                - "8080:80"
            restart: always
            environment:
                DEBUG: 0
                SECRET_KEY: "not-really-secret-key"
                DATABASE_DSN: postgresql://nsnd:nsnd@db:5432/nsnd
                ALLOWED_HOSTS: '*'
                MEDIA_ROOT: /media
                THUMBNAIL_CACHE_DIR: /thumbnails

    volumes:
        dbdata:
        media:
        thumbnails:

    ```

2. Run both the database and the application by a simple `up` command:

        docker-compose up -d

3. Run migrations (in case there are some DB schema changes):

        docker-compose exec --user nsnd website sh -c "django-admin migrate"


*Note*: You can easily update the app by the image tag in the compose file. Make
sure to re-run migrations when updating.

## Running django commands in the container

You can easily run it using `docker exec`. Just make sure you're running it under `nsnd` user. Otherwise,
things will break.

    docker-compose exec --user nsnd website django-admin migrate

