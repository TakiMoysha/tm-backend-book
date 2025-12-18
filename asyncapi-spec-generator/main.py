import uuid
import pytest
import msgspec
import logging
from django import setup
from django.urls import get_resolver, include, path
from django.conf import settings
from django.core.handlers import asgi

# ===========================================================
# asgi.py
# ===========================================================

from django_modern_rest.plugins.msgspec import MsgspecSerializer
from django_modern_rest.routing import Router
from django_modern_rest import Controller, Body

settings.configure(
    SECRET_KEY="secret",
    ROOT_URLCONF=__name__,
    DMR_SETTINGS={},
    ALLOWED_HOSTS="*",
    DEBUG=True,
)

setup()

app = asgi.ASGIHandler()


USERS_DB: list["UserModel"] = []

# ==========================================================================================


class MsgSpecUserCreateModel(msgspec.Struct):
    email: str


class UserModel(MsgSpecUserCreateModel):
    uid: uuid.UUID


class UserController(
    Controller[MsgspecSerializer],
    Body[MsgSpecUserCreateModel],
):
    async def get(self) -> UserModel:
        return UserModel(uid=uuid.uuid4(), email="L2rXt@example.com")


router = Router(
    [
        path("users/", UserController.as_view(), name="users"),
    ]
)

urlpatterns = [
    path("api/", include((router.urls, "demo"), namespace="api")),
]

# ===========================================================
# tests
# ===========================================================


@pytest.fixture(autouse=True)
def logging_config():
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


@pytest.fixture()
def logger():
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    return logging.getLogger(__name__)


def test_resolver(logger):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    resolver = get_resolver()
    print(resolver)
    logging.info(resolver)
    logging.warning(resolver)
    logger.info(resolver)
    logger.warning(resolver)
