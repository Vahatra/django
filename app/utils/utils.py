from django.utils.text import slugify as django_slugify


def slugify(s):
    return django_slugify(s).lower()


def slugify_username(s):
    return django_slugify(s).replace("-", "_")
