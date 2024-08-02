# send_email/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from emails import consumers
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'send_email.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/notifications/", consumers.EmailConsumer.as_asgi()),
        ])
    ),
})
