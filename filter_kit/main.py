"""Backend driven UI for filters page."""

# ===========================================================

from abc import ABC


class BaseFilterGroup(ABC): ...


class BaseField(ABC): ...


class StringField(BaseField):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()


class NumberField(BaseField): ...


class ChoicesField(BaseField): ...


class AddressField(BaseField): ...


# ===========================================================
# TESTS
# ===========================================================

import pytest


def test_main():
    assert True
