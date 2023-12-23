from django.http import HttpRequest


def custom_context(request: HttpRequest):
    return { "custom_context": "hello from context function" }
