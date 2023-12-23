from django.views.generic.base import TemplateView, RedirectView
from django.urls import path, re_path

urlpatterns = [
    path("react-vue/", TemplateView.as_view(template_name="webpack.html"), name="web.react-vue"),
    path("native/", TemplateView.as_view(template_name="native.html"), name="web.native"),

    re_path(r"^.*$", RedirectView.as_view(pattern_name="web.react-vue", permanent=False)),
] 
