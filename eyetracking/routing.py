from .wsgi import *
from email.mime import application
from django.urls import path 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import WSConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        #URLRouter(
            path('/ws/',WSConsumer.as_asgi())
        #)
    ),
})
# -b 0.0.0.0 -p 8443

# Django의 url 과 비슷하다 
# ws_urlpatterns = [
#     path('',WSConsumer.as_asgi()),
# ]
