from django.http import HttpRequest
from health_check.views import MainView

from django.http.response import HttpResponse, JsonResponse


class HealthCheckCustomView(MainView):
    template_name = "health_check.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        plugins = []
        status = 200

        if request.headers.get("X_FORMAT", '') == "json":
            print("JSON")
            return self.render_to_response_json(plugins, status)

        return self.render_to_response(plugins, status)

    def render_to_response(self, plugins, status: int) -> HttpResponse:
        return HttpResponse("COOL" if status == 200 else "SWEATY",status=status)

    def render_to_response_json(self, plugins, status: int) -> HttpResponse:
        return JsonResponse(
            { str(p.identifier()): "COOL" if status == 200 else "SWEATY" for p in plugins},
            status=status
        )

