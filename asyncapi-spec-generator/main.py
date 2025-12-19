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

asgi = asgi.ASGIHandler()


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
        """bag with paring GET body"""
        return UserModel(uid=uuid.uuid4(), email="L2rXt@example.com")

    async def post(self) -> UserModel:
        return UserModel(uid=uuid.uuid4(), email=self.parsed_body.email)


class AccountController(
    Controller[MsgspecSerializer],
):
    __asyncapi_spec__ = {}

    async def get(self) -> dict:
        return {}


router = Router(
    [
        path("users/", UserController.as_view(), name="users"),
        path("accounts/", AccountController.as_view(), name="accounts"),
    ]
)

urlpatterns = [
    path("api/", include((router.urls, "demo"), namespace="api")),
]

# ===========================================================
# implementation.py
# ===========================================================

CONTENT_TYPE = "application/cloudevents+json"


def asyncapi_channel():
    """decorator for function-based views"""


def parser_django_view(pattern, prefix=""):
    route_info = {}

    # full_path
    pattern_str = str(pattern.pattern)
    full_path = prefix + pattern_str
    route_info["path"] = full_path
    route_info["name"] = pattern.name if hasattr(pattern, "name") else None

    # TODO: test for both conditions
    if not hasattr(pattern, "callback") or pattern.callback is None:
        return route_info

    callback = pattern.callback
    route_info["view"] = {
        "name": callback.__name__ if hasattr(callback, "__name__") else str(callback),
        "module": callback.__module__ if hasattr(callback, "__module__") else None,
    }

    # TODO: test with and without view_class endpoint
    if not hasattr(callback, "view_class"):
        route_info["view"]["class"] = None
        route_info["view"]["class_module"] = None
        return route_info

    view_class = callback.view_class
    route_info["view"]["class"] = view_class.__name__
    route_info["view"]["class_module"] = view_class.__module__

    methods = []
    for method in ["get", "post", "put", "patch", "delete", "head", "options"]:
        # TODO: test methods parsing
        if not hasattr(view_class, method):
            continue

        method_func = getattr(view_class, method)
        method_info = {
            "method": method.upper(),
            "handler": method_func.__name__,
        }

        # TODO: test annotations parsing
        if hasattr(method_func, "__annotations__"):
            annotations = method_func.__annotations__
            method_info["annotations"] = {k: str(v) for k, v in annotations.items()}

            # TODO: test return type
            if "return" in annotations:
                method_info["return_type"] = str(annotations["return"])

        # TODO: test docstring parsing
        if method_func.__doc__:
            method_info["docstring"] = method_func.__doc__.strip()

        methods.append(method_info)

    route_info["methods"] = methods

    #  Body, Query, Path параметрах из MRO и __orig_bases__
    parameters = {}
    # TODO: test generic types
    if hasattr(view_class, "__orig_bases__"):
        for base in view_class.__orig_bases__:
            base_name = getattr(base, "__name__", str(base))

            # Извлекаем Body тип
            if "Body" in str(base):
                if not hasattr(base, "__args__"):
                    continue

                body_type = base.__args__[0] if base.__args__ else None

                if not body_type:
                    continue

                parameters["body"] = {
                    "type": body_type.__name__ if hasattr(body_type, "__name__") else str(body_type),
                    "module": body_type.__module__ if hasattr(body_type, "__module__") else None,
                }

                # TODO: test msgspec struct files
                if hasattr(body_type, "__struct_fields__"):
                    fields = {}
                    for field_name in body_type.__struct_fields__:
                        field_type = body_type.__annotations__.get(field_name)
                        fields[field_name] = str(field_type) if field_type else "unknown"
                    parameters["body"]["fields"] = fields

    # TODO: test MRO resolving
    for base in view_class.__mro__:
        if base.__name__ in ["Query", "Path"]:
            param_type = base.__name__.lower()
            parameters[param_type] = {
                "type": base.__name__,
                "class": str(base),
            }

    if parameters:
        route_info["view"]["parameters"] = parameters

    return route_info


# ===========================================================
# tests
# ===========================================================


@pytest.fixture(autouse=True)
def logging_config():
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def test_msgspec_schema_generator():
    schema = msgspec.json.schema(MsgSpecUserCreateModel)
    logging.info(schema)


def parse_url_patterns(url_patterns, current_prefix=""):
    """Recursively through all url patterns to find endpoints"""
    routes = []

    def _is_endpoint(ptn):
        return hasattr(ptn, "callback") and not hasattr(ptn, "url_patterns")

    def _is_include_router(ptn):
        return hasattr(ptn, "url_patterns")

    for pattern in url_patterns:
        if _is_endpoint(pattern):
            route = parser_django_view(pattern, current_prefix)
            routes.append(route)

        elif _is_include_router(pattern):
            pattern_str = str(pattern.pattern)
            new_prefix = current_prefix + pattern_str

            if hasattr(pattern, "namespace") and pattern.namespace:
                namespace_info = {
                    "path": new_prefix,
                    "type": "namespace",
                    "namespace": pattern.namespace,
                }
                routes.append(namespace_info)

            routes.extend(parse_url_patterns(pattern.url_patterns, new_prefix))

    return routes


def test_resolver():
    import json

    resolver = get_resolver()
    logging.info(f"Resolver: {resolver}")

    # Парсим маршруты
    routes = parse_url_patterns(resolver.url_patterns)

    # Выводим в виде JSON
    routes_json = json.dumps(routes, indent=2, ensure_ascii=False)
    logging.info(f"\n=== Parsed Routes ===\n{routes_json}")

    # Дополнительная статистика
    endpoint_count = sum(1 for r in routes if r.get("type") != "namespace")
    namespace_count = sum(1 for r in routes if r.get("type") == "namespace")

    logging.info(f"\n=== Statistics ===")
    logging.info(f"Total endpoints: {endpoint_count}")
    logging.info(f"Total namespaces: {namespace_count}")
    logging.info(f"Total routes: {len(routes)}")
