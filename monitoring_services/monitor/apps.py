from django.apps import AppConfig

from health_check.plugins import plugin_dir


class MonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitor'

    def ready(self) -> None:
        from .health_backend import MyHealthCheckBackend
        plugin_dir.register(MyHealthCheckBackend)
        return super().ready()
