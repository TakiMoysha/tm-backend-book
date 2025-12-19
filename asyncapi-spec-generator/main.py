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
    """Used in tests, should contain actual schema"""

    __json_schema__ = {
        "title": "MsgSpecUserCreateModel",
        "properties": {"email": {"type": "string"}},
        "x-module": "main",
    }

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

from typing import Any, Dict, TypedDict

CONTENT_TYPE = "application/cloudevents+json"

type WIP = Any


class AsyncApiIdObject(str):
    """Required  URN format or link to application sources"""


class AsyncApiInfoObject(TypedDict):
    title: str
    version: str
    description: str | None
    termsOfService: str | None
    contact: WIP
    license: WIP
    tags: WIP
    externalDocs: WIP


class AsyncApiServerObject(TypedDict):
    """

    Example:
    ```
    {
     "host": "kafka.in.company.edu:9092",
     "description": "Stage kafka server",
     "protocol": "kafka",
     "protocolVersion": "3.2",
    }
    ```
    """

    host: str
    protocol: str
    protocolVersion: str | None
    pathname: str | None
    description: str | None
    title: str | None
    summary: str | None
    variables: WIP
    security: WIP
    tags: WIP
    externalDocs: WIP
    bindings: WIP


class AsyncApiServersObject(Dict[str, AsyncApiServerObject]):
    pass


TYPE_MAP = {
}

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

    #  Body, Query, Path from MRO & __orig_bases__
    parameters = {}
    # TODO: test generic types
    if hasattr(view_class, "__orig_bases__"):
        for base in view_class.__orig_bases__:
            base_name = getattr(base, "__name__", str(base))

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


def parse_url_patterns(url_patterns, current_prefix=""):
    """Recursively through all url patterns to find endpoints

    Args:
        url_patterns: url patterns
        current_prefix: current prefix

    Returns:
        list: List[AsyncApiRouter] - list of every full-path routes and asyncapi info
    """
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


def msgspec_struct_to_json_schema(struct_type):
    """
    Args:
        struct_type: msgspec.Struct

    Returns:
        dict: JSON Schema представление структуры
    """
    base_schema = msgspec.json.schema(struct_type)
    type_name = struct_type.__name__

    if "$defs" in base_schema and type_name in base_schema["$defs"]:
        schema = base_schema["$defs"][type_name].copy()
    else:
        schema = {k: v for k, v in base_schema.items() if k != "$defs"}

    schema["title"] = type_name

    if struct_type.__doc__:
        schema["description"] = struct_type.__doc__.strip()

    schema["x-module"] = struct_type.__module__

    if hasattr(struct_type, "__struct_fields__"):
        properties = schema.get("properties", {})

        for field_name in struct_type.__struct_fields__:
            if field_name not in properties:
                continue

            field_type = struct_type.__annotations__.get(field_name)

            if field_type:
                properties[field_name]["x-python-type"] = str(field_type)

    return schema


def build_asyncapi_spec(routes, info=None, servers=None):
    """WIP

    Args:
        routes: AsyncApiRoutersList from parse_url_patterns
        info: AsyncApiInfoObject - see asyncapi specification
        servers: AsyncApiServersObject - see asyncapi specification

    Returns:
        dict: AsyncAPISpecJson - Ready AsyncAPI specification
    """

    info_stub = {
        "title": "Django Modern REST API",
        "version": "1.0.0",
        "description": "AsyncAPI specification generated from Django Modern REST controllers",
    }
    servers_stub: AsyncApiServersObject = {
        "development": {
            "host": "localhost:8000",
            "protocol": "http",
            "description": "Development server",
        }
    }
    asyncapi_spec = {
        "asyncapi": "3.0.0",
        "info": info or info_stub,
        "servers": servers or servers_stub,
        "channels": {},
        "operations": {},
        "components": {"schemas": {}, "messages": {}},
    }

    # Собираем все уникальные типы для schemas
    collected_types = {}

    # Обрабатываем каждый маршрут
    for route in routes:
        # skip namespace
        if route.get("type") == "namespace":
            continue

        path = route.get("path", "")
        route_name = route.get("name", path.replace("/", "_"))
        view_info = route.get("view", {})
        methods = route.get("methods", [])

        # WARN: WIP, review - channels generator
        channel_id = f"channel_{route_name}"
        asyncapi_spec["channels"][channel_id] = {"address": path, "messages": {}}

        # WARN: WIP, review - methods processing
        for method_info in methods:
            http_method = method_info.get("method", "").lower()

            # options it is support method
            if http_method == "options":
                continue

            # GET, DELETE - Receive
            # POST, PUT, PATCH - Send
            operation_type = "receive" if http_method in ["get", "delete", "head"] else "send"

            operation_id = f"{route_name}_{http_method}"
            message_id = f"{operation_id}_message"

            message: Dict[str, str | dict] = {
                "name": f"{route_name} {http_method.upper()}",
                "title": f"{http_method.upper()} {path}",
            }

            # description as docstring
            if method_info.get("docstring"):
                message["description"] = method_info["docstring"]

            # payload - request_body for Send, response for Receive
            payload_schema: Dict[str, str] | None = None

            if operation_type == "send":
                parameters = view_info.get("parameters", {})
                if "body" in parameters:
                    body_type_name = parameters["body"]["type"]

                    # WARN: WIP, this is a stub, next step is to resolve type
                    payload_schema = {"$ref": f"#/components/schemas/{body_type_name}"}

                    # collect type for schemas generation
                    if body_type_name not in collected_types:
                        collected_types[body_type_name] = parameters["body"]
            else:
                return_type = method_info.get("return_type", "")
                if return_type and "class" in return_type:
                    # TODO: added test for return_type name
                    type_name = return_type.__class__.__name__
                    payload_schema = {"$ref": f"#/components/schemas/{type_name}"}

                    if type_name not in collected_types:
                        collected_types[type_name] = {"type": type_name}

            if payload_schema:
                message["payload"] = payload_schema

            # WARN: WIP, review:
            asyncapi_spec["components"]["messages"][message_id] = message
            asyncapi_spec["channels"][channel_id]["messages"][message_id] = {
                "$ref": f"#/components/messages/{message_id}"
            }
            operation = {
                "action": operation_type,
                "channel": {"$ref": f"#/channels/{channel_id}"},
                "summary": f"{http_method.upper()} operation for {path}",
            }

            # WARN: WIP
            if operation_type == "send":
                operation["messages"] = [{"$ref": f"#/channels/{channel_id}/messages/{message_id}"}]
            else:
                operation["messages"] = [{"$ref": f"#/channels/{channel_id}/messages/{message_id}"}]

            asyncapi_spec["operations"][operation_id] = operation

    return asyncapi_spec, collected_types


def resolve_and_add_schemas(asyncapi_spec, collected_types, type_map=None):
    """
    Args:
        asyncapi_spec: AsyncApiSpec
        collected_types: types from routes
        type_map: 

    Returns:
        dict: обновленная AsyncAPI спецификация
    """
    # WARN: WIP
    for type_name, type_info in collected_types.items():
        if type_map and type_name in type_map:
            type_class = type_map[type_name]

            # TODO: only for msgspec.Struct
            if hasattr(type_class, "__struct_fields__"):
                schema = msgspec_struct_to_json_schema(type_class)
                asyncapi_spec["components"]["schemas"][type_name] = schema
            else:
                asyncapi_spec["components"]["schemas"][type_name] = {
                    "type": "object",
                    "title": type_name,
                    "x-python-type": str(type_class),
                }
        else:
            asyncapi_spec["components"]["schemas"][type_name] = {
                "type": "object",
                "title": type_name,
                "description": f"Schema for {type_name} (not resolved)",
            }

    return asyncapi_spec


def serialize_to_yaml(asyncapi_spec, sort_keys=False):
    """
    Args:
        asyncapi_spec: AsyncApiSpec
        sort_keys:

    Returns:
        str:
    """
    import yaml

    class CustomDumper(yaml.SafeDumper):
        pass

    def str_representer(dumper, data):
        if "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    CustomDumper.add_representer(str, str_representer)

    yaml_content = yaml.dump(
        asyncapi_spec,
        Dumper=CustomDumper,
        default_flow_style=False,
        sort_keys=sort_keys,
        allow_unicode=True,
        indent=2,
        width=120,
    )

    return yaml_content


def export_to_file(asyncapi_spec, output_path="asyncapi.yaml", sort_keys=False):
    """
    Args:
        asyncapi_spec: AsyncApiSpec
        output_path: outputfile
        sort_keys: сортировать ключи в алфавитном порядке

    Returns:
        str: Path
    """
    from pathlib import Path

    yaml_content = serialize_to_yaml(asyncapi_spec, sort_keys=sort_keys)
    output_file = Path(output_path)
    output_file.write_text(yaml_content, encoding="utf-8")

    return output_file.absolute()


def generate_asyncapi_from_django(url_patterns, output_path="asyncapi.yaml", info=None, servers=None, sort_keys=False):
    """
    Args:
        url_patterns: Router or urlpatterns
        output_path: output file
        info: AsyncApiInfoObject
        servers: AsyncApiServerObject
        sort_keys: сортировать ключи в алфавитном порядке

    Returns:
        tuple: (asyncapi_spec dict, output_file_path str)
    """
    routes = parse_url_patterns(url_patterns)
    asyncapi_spec, collected_types = build_asyncapi_spec(routes, info, servers)
    logging.info(f"Collected types: {collected_types}")
    asyncapi_spec = resolve_and_add_schemas(asyncapi_spec, collected_types)
    output_file = export_to_file(asyncapi_spec, output_path, sort_keys)
    return asyncapi_spec, output_file


# ===========================================================
# tests
# ===========================================================


@pytest.fixture(autouse=True)
def logging_config():
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


from unittest import TestCase


def test_should_convert_msgspec_to_json_schema():
    import json

    schema = msgspec_struct_to_json_schema(MsgSpecUserCreateModel)

    schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
    logging.info(f"\nMsgSpecUserCreateModel Schema:\n{schema_json}")

    # TestCase().assertDictEqual(
    #     MsgSpecUserCreateModel.__json_schema__,
    #     schema,
    # )
    assert "title" in schema and schema["title"] == "MsgSpecUserCreateModel"
    assert "properties" in schema and "email" in schema["properties"]
    assert schema["properties"]["email"]["type"] == "string"
    assert "x-module" in schema and schema["x-module"] == "main"


def test_asyncapi_builder():
    asyncapi_spec, collected_types = build_asyncapi_spec(
        parse_url_patterns(get_resolver().url_patterns),
        info={"title": "Test API", "version": "1.0.0", "description": "Test AsyncAPI specification"},
    )

    logging.info(f"{collected_types=}")
    asyncapi_spec = resolve_and_add_schemas(asyncapi_spec, collected_types)
    logging.info(f"{asyncapi_spec=}")


# ==========================================================================================


def test_target():
    import json

    resolver = get_resolver()
    logging.info(f"Resolver: {resolver}")

    routes = parse_url_patterns(resolver.url_patterns)

    routes_json = json.dumps(routes, indent=2, ensure_ascii=False)
    logging.info(f"ROUTER_JSON:\n{routes_json}")

    endpoint_count = sum(1 for r in routes if r.get("type") != "namespace")
    namespace_count = sum(1 for r in routes if r.get("type") == "namespace")

    logging.info(f"STAT:\n\t{endpoint_count=}\n\t{namespace_count=}\n{len(routes)=}")


# ==========================================================================================


# register mark side_effects


# @pytest.mark.skip("this is use-case, not test")
@pytest.mark.scenario
@pytest.mark.side_effects
def test_full_create_asyncapi_spec():
    from pathlib import Path

    output_path = "asyncapi.yaml"
    resolver = get_resolver()

    asyncapi_spec, output_file = generate_asyncapi_from_django(
        resolver.url_patterns,
        output_path=output_path,
        info={
            "title": "Django Modern REST API",
            "version": "0.8.3",
            "description": "Auto-generated AsyncAPI specification from Django Modern REST controllers",
        },
        servers={
            "development": {"host": "localhost:8000", "protocol": "http", "description": "Development server"},
            "production": {"host": "api.example.com", "protocol": "https", "description": "Production server"},
            "queue": {"host": "localhost:5672", "protocol": "amqp", "description": "RabbitMQ server"},
        },
    )

    output_path_obj = Path(output_file)
    assert output_path_obj.exists(), f"File not created: {output_path_obj}"
