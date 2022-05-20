from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.basic, name='index'),
    path('', views.video, name='video'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('<int:pk>/', views.mypage, name='mypage'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('lecture/', views.lecture, name='lecture'),
    path('lecture_mark_toggle/<int:lecture_id>/',
         views.lecture_mark_toggle, name="lecture_mark_toggle")
]