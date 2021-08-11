import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

import message_chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipal.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            message_chat.routing.messaging_urlpatterns
        )
    ),
})
