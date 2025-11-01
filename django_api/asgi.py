import uuid

import pydantic
import msgspec
from django.conf import settings
from django.core.handlers import asgi
from django.urls import include, path

from django_modern_rest import Body, Controller, Headers
from django_modern_rest.plugins.pydantic import PydanticSerializer
from django_modern_rest.plugins.msgspec import MsgspecSerializer
from django_modern_rest.routing import Router


settings.configure(
    SECRET_KEY="secret",
    # Keep it as is
    ROOT_URLCONF=__name__,
    # Required options but feel free to configure as you like
    DMR_SETTINGS={},
    ALLOWED_HOSTS="*",
    DEBUG=True,
)

app = asgi.ASGIHandler()


class UserCreateModel(msgspec.Struct):
    email: str


class UserModel(UserCreateModel):
    uid: uuid.UUID


class HeaderModel(pydantic.BaseModel):
    consumer: str = pydantic.Field(alias="X-API-Consumer")


class UserController(
    Controller[MsgspecSerializer],
    Body[UserCreateModel],
    Headers[HeaderModel],
):
    async def get(self) -> UserModel:
        return UserModel(uid=uuid.uuid4(), email="L2rXt@example.com")

    async def post(self) -> UserModel:
        assert self.parsed_headers.consumer == "my-api"
        return UserModel(uid=uuid.uuid4(), email=self.parsed_body.email)


router = Router(
    [
        path("users", UserController.as_view(), name="users"),
    ]
)
urlpatterns = [
    path("api/", include((router.urls, "your_app"), namespace="api")),
]
