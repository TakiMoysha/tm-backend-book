from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import base_common_view 

urlpatterns = [
    path('', base_common_view),
    path('template', TemplateView.as_view(template_name="index.html")),
]
