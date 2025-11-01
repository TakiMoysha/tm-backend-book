import logging
import uuid
from typing import final

import msgspec
import pydantic
from django.conf import settings
from django.core.handlers import asgi
from django.urls import include
from django.urls import path
from django_modern_rest import Body
from django_modern_rest import Controller
from django_modern_rest.plugins.msgspec import MsgspecSerializer
from django_modern_rest.plugins.pydantic import PydanticSerializer
from django_modern_rest.routing import Router
from django_modern_rest.test import DMRRequestFactory
from polyfactory.factories.msgspec_factory import MsgspecFactory
from polyfactory.factories.pydantic_factory import ModelFactory

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

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


# ==========================================================================================


class PydanticUserCreateModel(pydantic.BaseModel):
    email: str


class MsgSpecUserCreateModel(msgspec.Struct):
    email: str


# UserCreateModel = PydanticUserCreateModel
UserCreateModel = MsgSpecUserCreateModel
Serializer = PydanticSerializer
Serializer = MsgspecSerializer
# # ==========================================================================================
#


class UserModel(UserCreateModel):
    uid: uuid.UUID


# class HeaderModel(pydantic.BaseModel):
#     consumer: str = pydantic.Field(alias="X-API-Consumer")


users_db: list[UserModel] = []


class UserController(
    Controller[Serializer],
    Body[UserCreateModel],
    # Headers[HeaderModel],
):
    def get(self) -> UserModel:
        return UserModel(uid=uuid.uuid4(), email="L2rXt@example.com")

    # def post(self) -> UserModel | ResponseSpec:
    #     # check if ritght consumer, or return bad request
    #     logging.warning(f"{self.parsed_headers};{self.parsed_body}")
    #     if self.parsed_headers.consumer != "my-api":
    #         logging.warning("Consumer is not allowed")
    #         return ResponseSpec(return_type={}, status_code=HTTPStatus.FORBIDDEN)
    #
    #     logging.warning("Consumer is not allowed")
    #     user = UserModel(uid=uuid.uuid4(), email=self.parsed_body.email)
    #     users_db.append(user)
    #     return user


router = Router(
    [
        path("users/", UserController.as_view(), name="users"),
    ]
)
urlpatterns = [
    path("api/", include((router.urls, "your_app"), namespace="api")),
]

# ===========================================================
# testing
# ===========================================================

import pytest
from django_modern_rest.test import DMRClient


@pytest.fixture
def dmr_client() -> "DMRClient":
    return DMRClient()


@pytest.fixture
def dmr_rf() -> "DMRRequestFactory":
    from django_modern_rest.test import DMRRequestFactory

    return DMRRequestFactory()


# ==========================================================================================
@final
class MsgSpecUserCreateModelFactory(MsgspecFactory[MsgSpecUserCreateModel]):
    __check_model__ = True


@final
class PydanticUserCreateModelFactory(ModelFactory[PydanticUserCreateModel]):
    __check_model__ = True


# ==========================================================================================


import django.test.client


# def test_user_controller_with_pydantic(dmr_client: DMRClient, dmr_rf: DMRRequestFactory) -> None:
    # request_data = PydanticUserCreateModelFactory.build()
    # all_users = UserController.as_view()(dmr_rf.get("/api/users/"))
    # logging.warning(all_users)

    # request = dmr_rf.post("/api/users/", data=request_data, headers={"X-API-Consumer": "my-api"})
    # response: ResponseSpec = UserController.as_view()(request)
    #
    # assert response.status_code == 200, response

def test_user_controller_with_msgspec(dmr_client: DMRClient, dmr_rf: DMRRequestFactory) -> None:
    request_data = MsgSpecUserCreateModelFactory.build()
    all_users = UserController.as_view()(dmr_rf.get("/api/users/"))
    logging.warning(all_users)
#     # request = dmr_rf.post("/api/users/", data=request_data, headers={"X-API-Consumer": "my-api"})
#     # response: ResponseSpec = UserController.as_view()(request)
#
#     # assert response.status_code == 200, response
