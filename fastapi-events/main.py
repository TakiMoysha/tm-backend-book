from enum import StrEnum, auto
from typing import Any, Callable


class EventSpace(StrEnum):
    userspace = auto()
    support = auto()
    infra = auto()


_event_registry = {}


def register_event():
    def decorator(func):
        _event_registry[func.__name__] = func
        return func

    return decorator


# ==========================================================================================

from unittest.mock import MagicMock


def try_event(event: Callable, *, OutboxEventManager: Any = MagicMock()):
    try:
        event()
    except BaseEventError as err:
        OutboxEventManager.save_for_retry({"event": event, "params": [], "error": err})
    except Exception as err:
        return {"status": "error", "details": str(err)}


# ==========================================================================================

from fastapi.middleware import BaseHTTPMiddleware


class PostEventMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        for domain, event in request.state.events:
            handler = _event_registry.get(domain)
            if not handler:
                continue

            res = await try_event(handler(event))

        return response

