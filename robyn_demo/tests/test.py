from abc import ABC, abstractmethod
from typing import Callable, List

from jinja2 import Environment, FileSystemLoader
from robyn import Headers, Response, Robyn, status_codes
from robyn.router import Route


class JinjaTemplate:
    def __init__(self, directory, encoding="utf-8", followlinks=False) -> None:
        self.env: Environment = Environment(loader=FileSystemLoader(searchpath=directory, encoding=encoding, followlinks=followlinks))
        self.add_function_to_globals("get_function_url", self.get_function_url)
        self.robyn: Robyn | None = None

    def add_function_to_globals(self, name: str, func: Callable):
        self.env.globals[name] = func

    def set_robyn(self, robyn: Robyn) -> None:
        self.robyn = robyn

    def get_function_url(self, function_name: str, route_type: str = "GET") -> str:
        if self.robyn is None:
            return "get_function_url needs set_robyn"

        routes: List[Route] = self.robyn.router.get_routes()
        for r in routes:
            if r.function.handler.__name__ == function_name and str(r.route_type) == f"HttpMethod.{route_type}":
                return r.route

        return "route not found in Robyn router"

    def render_template(self, template_name, **kwargs) -> Response:
        rendered_template = self.env.get_template(template_name).render(**kwargs)
        return Response(
            status_code=status_codes.HTTP_200_OK,
            description=rendered_template,
            headers=Headers({"Content-Type": "text/html; charset=utf-8"}),
        )


__all__ = ["JinjaTemplate"]
