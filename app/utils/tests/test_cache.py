import hashlib
import random
import time

import pytest

from app.users.models import User
from app.users.tests.factories import UserFactory
from app.utils.cache import cache_result_ttl
from django.db.models import Model
from django.utils.encoding import force_bytes


def model_key_generator(*args) -> str:
    return ":".join((str(arg.pk) if isinstance(arg, Model) else "" for arg in args))


@cache_result_ttl(100, prefix="test", key_generator=model_key_generator)
def a(user1: User, user2: User, user3: User):
    return


@pytest.mark.django_db
def test_key():
    user1 = UserFactory().create()
    user2 = UserFactory().create()
    user3 = UserFactory().create()
    result = a.get_key(user1, user2, user3)
    expected = (
        "test"
        + hashlib.md5(force_bytes(model_key_generator(user1, user2, user3))).hexdigest()
    )
    assert expected == result


@cache_result_ttl(100)
def b(start, end):
    return random.randint(start, end)


def test_invalidate():
    first = b(1, 100)
    second = b(1, 100)
    assert first == second
    b.invalidate(1, 100)
    third = b(1, 100)
    assert third != first


@cache_result_ttl(2)
def c(start, end):
    return random.randint(start, end)


def test_timeout():
    first = c(101, 200)
    second = c(101, 200)
    assert first == second
    time.sleep(2.5)
    third = c(101, 200)
    assert third != first
