from django.urls import path

from . import views

urlpatterns = [
    path('', views.basic, name='index'),
    path('test/', views.classifyvideo, name='test')
]