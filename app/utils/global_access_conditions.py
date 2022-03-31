from .access_policy import has_some_perm


def some_perm(request, view, action) -> bool:
    """
    A pointles global access condition to demonstrate usage.
    """
    return has_some_perm(request.user)
