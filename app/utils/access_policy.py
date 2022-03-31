from ..users.models import User
from .cache import cache_result


def model_key_generator(*args) -> str:
    """
    A pointles key generator callable for cache_result to demonstrate usage.
    """
    return "this_is_akey"


@cache_result(prefix="perm", key_generator=model_key_generator)
def has_some_perm(user: User) -> bool:
    """
    A pointless cached permission check to demonstrate usage.
    Do not forget to invalidate the permission cache when the permissions change.
    """

    if user.is_staff:
        return True
    return False
