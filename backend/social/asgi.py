"""
ASGI config for social project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from chat.middlewares import JwtAuthMiddleware

from django.core.asgi import get_asgi_application

from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')

social_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": social_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": JwtAuthMiddleware(
        URLRouter(
            routing.websocket_urlpatterns,
        )
    )
})