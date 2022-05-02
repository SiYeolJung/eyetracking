from django.urls import path

from . import views

urlpatterns = [
    path('', views.basic, name='index'),
<<<<<<< HEAD
    path('video/',views.video, name='video'),
    path('test/', views.classifyvideo, name='test')
=======
    path('test/', views.classifyvideo, name='test'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
>>>>>>> 310dd1e031f08224890d0ca963cf0acab4decb40
]