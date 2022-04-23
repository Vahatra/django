# DRF base project

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A base project for building `APIs` using `django` and `drf`.

Generated by [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django/) and added/modified `things`.

License: MIT

## The stack

- Python [3.9](https://docs.python.org/).
- Django [3.2.12](https://docs.djangoproject.com/).
- DRF [3.13.1](https://www.django-rest-framework.org/).
- Celery [5.2.3](http://docs.celeryproject.org/en/latest/index.html).
- Authentications: `JWT`.
- pytest [7.1.1](https://github.com/pytest-dev/pytest).
- drf-spectacular [0.22.0](https://github.com/tfranzel/drf-spectacular).
- drf-access-policy [1.1.0](https://rsinger86.github.io/drf-access-policy/).
- Packaging and dependency management using [Poetry](https://python-poetry.org/).
- ... more detail in the [pyproject.toml](pyproject.toml) file.

- Redis via [official Docker image](https://hub.docker.com/_/redis).
- Postgres [13.2](https://www.postgresql.org/) via [official Docker image](https://hub.docker.com/_/postgres).
- `traefik` or `nginx` (no ssl)

## Docker

- **[local.yml](local.yml)** for local development.
- **[prod.yml](prod.yml)** with `traefik`
- Can use **[traefik.nossl.yml](compose/production/traefik/traefik.nossl.yml)** as a file provider for [traefik's Dockerfile](compose/production/traefik/Dockerfile#L5) to have the `dashboard` and no `ssl`.
- **[prod.nginx.yml](prod.nginx.yml)** with `nginx`, no `ssl`.



## The things

### Create app

Create an app based on a **[custom template](app/core/app_template/)**.

    $ python manage.py startapp_api my_app_name

### Factory

A **[little class](app/utils/factory.py)** that can be inherited and used with a `ModelSerializer` for creating dummy data, example:

```python
@dataclass
class SomeFactory(SerializerFactory):
    serializer_class = SomeSerializer
    an_attribute: str = None
    another_attribute: str = None

    def __post_init__(self):
        if self.an_attribute is None:
            self.an_attribute = fake.job()
        if self.another_attribute is None:
            self.another_attribute = fake.email()

# tests
def test_some():
    # create
    some: Some = SomeFactory(an_attribute="test").create()
    # OR
    some_factory: SomeFactory = SomeFactory(an_attribute="test")
    # create
    some: Some = some_factory.create()
    # update
    some: Some = some_factory.update(data={"an_attribute": "another_test"})
    # get desirialized data (JSON)
    data = some_factory.get_data()
```

### Caching

Helper **[fucntions](app/utils/cache.py)** for caching a function.

Can specify the `timeout`, `prefix` and a `key_generator`:

```python
def some_key_generator(*args) -> str:
    return "this_is_akey"

# cahche with the default timeout set in the settings.
@cache_result()
def some_function(prefix="prefix", key_generator=some_key_generator):
    return "this is a result"

# cahche with the 100s timeout.
@cache_result_ttl(100)
def some_function(prefix="prefix", key_generator=some_key_generator):
    return "this is a result"
```

### Download file

Helper **[fucntion](app/utils/send_file.py)** for downloading file.

```python
# settings
SENDFILE_BACKEND = "app.utils.send_file.NginxBackend"

# usage
@action(["get"], detail=True)
def download(self, request, *args, **kwargs):
    instance = self.get_object()
    if not instance.a_file.name:
        return Response("no file", status=status.HTTP_404_NOT_FOUND)

    return send_file(request, instance.doc_file.path)
```

### User app

User app with basic endpoints (**[views.py](app/users/views.py)**):

- `GET /user/`
- `POST /user/`
- `GET /user/{uuid}/`
- `PATCH /user/{uuid}/`
- `PUT /user/{uuid}/`
- `DELETE /user/{uuid}/`
- `POST /user/{uuid}/activate`
- `POST /user/{uuid}/deactivate`
- `POST /user/{uuid}/profile/`
- `GET /user/{uuid}/profile/`
- `PATCH /user/{uuid}/profile/`
- `PUT /user/{uuid}/profile/`
- `DELETE /user/{uuid}/profile/`
- `GET /user/me/`
- `PATCH /user/me/`
- `PUT /user/me/`
- `DELETE /user/me/`
- `POST /user/reset_password/`
- `POST /user/reset_password_comfirm/`

## Run

### Local

```bash
# virtualenv
poetry shell
# install dependencies
poetry install

# database
docker-compose -f local.yml up -d postgres

# rename the environment file
mv .env.example .env

# migrations
python manage.py migrate
# run
python manage.py runserver_plus
```

### Local (Docker)
```bash
docker-compose -f local.yml up -d
```

### Production
```bash
# rename the environment files and set the environment variables
mv .envs/.production/.postgres.example .envs/.production/.postgres
mv .envs/.production/.django.example .envs/.production/.django

docker-compose -f prod.yml up -d
```
