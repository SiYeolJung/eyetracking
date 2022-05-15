from email.mime import application
from django.urls import path 

from .consumers import WSConsumer
# from .consumers import BoolWS

# Django의 url 과 비슷하다 
ws_urlpatterns = [
    path('ws/some_url/',WSConsumer.as_asgi())
    # path('ws/',BoolWS.as_asgi())
    # path('ws/',BoolWS.as_asgi())
    
]