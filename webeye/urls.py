from django.urls import path
from django.http import HttpResponse

from . import views

def heart_beat(request):
    return HttpResponse("OK!", content_type='text/plain')

urlpatterns = [
    path('^heart_beat/', heart_beat),
    path('index/', views.basic, name='index'),
    path('', views.video, name='video'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('<int:pk>/', views.mypage, name='mypage'),
    path('lecture/', views.lecture, name='lecture'),
    path('project/', views.project, name='project'),
    path('lecture_mark_toggle/<str:course>/',
         views.lecture_mark_toggle, name="lecture_mark_toggle"),
    path('<str:course>/', views.lecture_list, name='lecture_list'),
    path('to_video/<int:lid>/', views.to_video, name='to_video')
]