"""
ASGI config for YouYuanUBan_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YouYuanUBan_backend.settings')

application = get_asgi_application()

#需要asgi则替换
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter(routing.websocket_urlpatterns),
# })
