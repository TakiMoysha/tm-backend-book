from django.contrib import admin
from django.urls import path, re_path, include

from monitor import views as monitor_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ht/", include("health_check.urls")),
    # re_path("ht/", monitor_views.HealthCheckCustomView.as_view(), name="health_check_custom"),
]
