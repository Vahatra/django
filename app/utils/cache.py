# based on https://github.com/peterbe/django-cache-memoize

import hashlib
from functools import wraps
from typing import Callable

from django.core.cache import cache
from django.utils.encoding import force_bytes

sentinel = object()


def cache_result(prefix: str = "", key_generator: Callable = None):
    """Decorator for caching the result of a funtion.
    timeout: Number of seconds to store the result if not None
    key_args: List of args' (models) name for forming the key, only use with models.
    prefix: Key prefix.
    key_generator: Custom cache key name generator.
    """

    def decorator(func):
        def _make_key(*args):
            key = key_generator(*args) if key_generator else ""
            _prefix = prefix if prefix else ""
            return (
                _prefix + hashlib.md5(force_bytes(func.__qualname__ + key)).hexdigest()
            )

        @wraps(func)
        def inner(*args, **kwargs):
            key = _make_key(*args)
            result = cache.get(key, sentinel)
            if result is sentinel:
                result = func(*args, **kwargs)
                cache.set(key, result)
            return result

        def invalidate(*args):
            key = _make_key(*args)
            cache.delete(key)

        def get_key(*args):
            return _make_key(*args)

        inner.invalidate = invalidate
        inner.get_key = get_key
        return inner

    return decorator


def cache_result_ttl(timeout: int, prefix: str = "", key_generator: Callable = None):
    """cache_result but with timeout."""

    def decorator(func):
        def _make_key(*args):
            key = key_generator(*args) if key_generator else func.__qualname__
            _prefix = prefix if prefix else ""
            return _prefix + hashlib.md5(force_bytes(key)).hexdigest()

        @wraps(func)
        def inner(*args, **kwargs):
            key = _make_key(*args)
            result = cache.get(key, sentinel)
            if result is sentinel:
                result = func(*args, **kwargs)
                cache.set(key, result, timeout)
            return result

        def invalidate(*args):
            key = _make_key(*args)
            cache.delete(key)

        def get_key(*args):
            return _make_key(*args)

        inner.invalidate = invalidate
        inner.get_key = get_key
        return inner

    return decorator
