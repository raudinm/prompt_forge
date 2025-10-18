"""
ASGI config for prompt_forge project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from forge.middleware.jwt_auth import JwtAuthMiddleware
import forge.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prompt_forge.settings')

# Django ASGI application
django_asgi_app = get_asgi_application()

# ASGI application with Channels
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JwtAuthMiddleware(
        URLRouter(
            forge.routing.websocket_urlpatterns
        )
    ),
})
