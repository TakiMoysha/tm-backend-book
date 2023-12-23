from django.http import HttpResponse
from django.template import loader


def base_common_view(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request), status=200)
