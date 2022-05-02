from django.urls import path

from . import views

urlpatterns = [
    path('', views.basic, name='index'),
    path('video/',views.video, name='video'),
    path('test/', views.classifyvideo, name='test')
]