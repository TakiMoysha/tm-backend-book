from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path("web/", TemplateView.as_view(template_name="index.html")),
]

