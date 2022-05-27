"""
ASGI config for eyetracking project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

# from django.core.asgi import get_asgi_application
from channels.routing import get_default_application
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter 
from channels.routing import URLRouter 

from eyetracking.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eyetracking.settings')

application = ProtocolTypeRouter({
    # 'http' : get_asgi_application(),
    'http' : get_default_application(),
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})
# django.setup()
# application = get_default_application()