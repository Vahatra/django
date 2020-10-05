# API

A django project.

## Architecture overview:

### Django Middleware

- Python **[3.8](https://docs.python.org/)**.
- Django **[3.0.7](https://docs.djangoproject.com/)**, installed via [pip](https://pypi.python.org/pypi) - official Python package index.
- Postgres **[11.3](https://www.postgresql.org/)**, installed via [official Docker image](https://hub.docker.com/_/postgres).
- Authentication using [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) and [python-social-auth](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html#).
- User management using [djoser](https://djoser.readthedocs.io/en/latest/index.html).

---

## First run:

### **Local developpement**

**ENV:** `.env` file.

Install and Activate your virtual environment:

```bash
# Your choice
```

Install `pip-tools`:

```bash
pip install pip-tools
```

Compile and Sync/Install the requirements:

```bash
pip-compile ./requirements/local.in
pip-sync ./requirements/local.txt
```

Copy initial settings for Django project:

```bash
cp ./.env.example ./.env
```

Run migrations:

```bash
python ./manage.py migrate
```

Create a superuser:

```bash
python ./manage.py createsuperuser
```

Run the django server:

```bash
python ./manage.py runserver
```

Browse the API using `Insomnia/Postman`.

or

Browse the API using `swagger`:

```bash
http://127.0.0.1:8000/swagger/ # Swagger
http://127.0.0.1:8000/redoc/ # Docs
```

### **Production using docker**

**ENV:** `.envs/.production/`

NOT IMPLEMENTED

---

## Management commands:

### **Commands for backend**

Run tests:

```bash
pytest
```

Check/Fix imports order with [isort](https://isort.readthedocs.io/en/latest/):

```bash
isort --check
isort -rc .
```

Foramting with [black](https://github.com/ambv/black):

```bash
black .
```

Linting with [flake8](https://github.com/PyCQA/flake8):

```bash
flake8
```

### **Update python requirements with pip-tools**

To work with a list of Python requirements we use [pip-tools](https://github.com/jazzband/pip-tools) utility.

To compile all requirement files:

```bash
pip-compile ./requirements/local.in
```

To synchronize requirements:

```bash
pip-sync ./requirements/local.txt
```
