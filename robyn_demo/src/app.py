from enum import Enum, StrEnum
from typing import Literal

from robyn import Robyn, logger
from robyn.robyn import HttpMethod


router = Robyn(__file__)



# app.start(port=8000)


def test(t: HttpMethod):
    t.value


__all__ = ["create_app"]


def create_app():
    router
