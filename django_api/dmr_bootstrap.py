from typing import TypedDict, Unpack, Any
import logging

from django.conf import settings
from django.core.handlers import asgi

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class DjangoSettings(TypedDict, total=False):
    SECRET_KEY: str
    DEBUG: bool
    ROOT_URLCONF: str
    ALLOWED_HOSTS: str
    DMR_SETTINGS: dict[str, Any]


def _bootstrap(**config: Unpack[DjangoSettings]) -> asgi.ASGIHandler:
    """Setup django settings config and initialize ASGI application."""
    settings.configure(**config)
    return asgi.ASGIHandler()


app = _bootstrap(
    SECRET_KEY="secret",
    DEBUG=True,
)
# or
config = DjangoSettings(
    {
        "SECRET_KEY": "secret",
        "DEBUG": True,
    }
)
app = _bootstrap(**config)

import msgspec
from django.urls import path
from django.http import HttpRequest, HttpResponse


def search_request_view(request: HttpRequest):
    response: Unpack[Any] = {}
    return HttpResponse(msgspec.msgpack.encode(response))


urlpatterns = [
    path("/", search_request_view),
]
