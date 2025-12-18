import logging
from typing import final

import msgspec
from django.conf import settings
from django.core.handlers import asgi
from django_modern_rest import Body
from django_modern_rest import Controller
from django_modern_rest.plugins.msgspec import MsgspecSerializer
from django_modern_rest.test import DMRClient, DMRRequestFactory
from polyfactory.factories.msgspec_factory import MsgspecFactory

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


class MsgSpecUserCreateModel(msgspec.Struct):
    email: str


class UserController(Controller[MsgspecSerializer], Body[MsgSpecUserCreateModel]):
    def get(self) -> MsgSpecUserCreateModel:
        return MsgSpecUserCreateModel(email="L2rXt@example.com")


@final
class MsgSpecUserCreateModelFactory(MsgspecFactory[MsgSpecUserCreateModel]):
    __check_model__ = True


def test_user_controller_with_msgspec(dmr_client: DMRClient, dmr_rf: DMRRequestFactory) -> None:
    request_data = MsgSpecUserCreateModelFactory.build()
    all_users = UserController.as_view()(dmr_rf.get("/api/users/"))
    logging.warning(all_users)
    assert all_users.status_code == 200, all_users
