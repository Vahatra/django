# based on https://github.com/johnsensible/django-sendfile

import os.path
from typing import Protocol

from django.conf import settings
from django.http import Http404, HttpResponse
from django.utils.module_loading import import_string
from django.views.static import serve

from .cache import cache_result


class CacheBackend(Protocol):
    def send(request, filename: str):
        ...


class NginxBackend:
    def send(request, filename):
        response = HttpResponse(status=200)
        response["Content-Type"] = ""
        relpath = os.path.relpath(filename, settings.DOCUMENT_ROOT)
        url = os.path.join(settings.DOCUMENT_URL, relpath)
        response["X-Accel-Redirect"] = url

        return response


class DjangoBackend:
    def send(request, filename):
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)

        return serve(request, basename, dirname)


@cache_result(prefix="send_file")
def _get_backend():
    backend = getattr(
        settings,
        "SEND_FILE_BACKEND",
        "app.utils.send_file.DjangoBackend",
    )
    module: CacheBackend = import_string(backend)

    return module.send


def send_file(request, filename):
    """
    Create a response to send file using backend configured in SEND_FILE_BACKEND
    """
    _send = _get_backend()

    if not os.path.exists(filename):
        raise Http404(f"{filename} does not exist")

    response = _send(request, filename)
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{os.path.basename(filename)}"'

    return response
