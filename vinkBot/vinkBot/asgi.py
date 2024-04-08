import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "vinkBot.settings")
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import bot.routing


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(bot.routing.websocket_urlpatterns),
    }
)
