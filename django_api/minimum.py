from django.conf import settings
from django.core.asgi import get_asgi_application

settings.configure(
    DEBUG=True,
    SECRET_KEY="secret",
    ROOT_URLCONF="minimum",
)

app = get_asgi_application()


urlpatterns = []
