"""!WARN: not working file"""

from unittest.mock import MagicMock
import pytest
import faker


def get_config(): ...


pytest_plugins = (
    "tests.hypothesis_fixtures",
    "tests.user_fixtures",
)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "runtime: mark test as runtime test",
    )


@pytest.fixture(name="faker", scope="session")
def fx_faker():
    return faker.Faker()


@pytest.fixture(name="app_config", scope="package")
def fx_app_config():
    config = MagicMock(get_config())  # or load settings
    if not config.server.testing:
        pytest.skip("TESTING_MODE is not enabled")

    return config

