import cv2 ## opencv-python 깔아야함
import numpy as np  ## numpy 깔아야함
import torch ## pytorch깔아야함 
import matplotlib.pyplot as plt
import json

from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from PIL import Image
from torchvision import transforms
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Users,Lecture,Scrap
import pymysql
import datetime
from django.views.decorators.csrf import csrf_exempt

now = datetime.datetime.now()
# Create your views here.

def basic(request):
    return render(request,'webeye/index.html')

def project(request):
    return render(request, 'webeye/project.html')

def video(request):
    return render(request,'webeye/main.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        rawPassword = request.POST['password1']

        if request.POST['password1'] == request.POST['password2']:

            #TODO: run transaction
            userObj = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)

            if Users.objects.all().exists():
                latestUser = Users.objects.all().order_by('-uid')[0]
                uid = latestUser.uid
            else:
                uid = 0

            Users.objects.create(uid = uid + 1, id = request.POST['username'], email = request.POST['email'], password = userObj.password, adddate = now.strftime('%Y-%m-%d %H:%M:%S'))

            auth.login(request, userObj)
            return redirect('/')
        return render(request, 'webeye/signup.html')
    return render(request, 'webeye/signup.html')

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'webeye/signin.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'webeye/signin.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def mypage(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    uid = Users.objects.get(id=user.username).uid
    myScrap = Scrap.objects.all().select_related('owner').select_related('lecture').filter(owner = uid, state = 1)
    courseList = []
    for lect in myScrap.values():    # 모든 lecture 돌면서
        temp = Lecture.objects.filter(lid=lect['lecture_id']).values()
        if temp[0]['course'] not in courseList:
            courseList.append(temp[0]['course'])
    print(courseList)
    return render(request, 'webeye/mypage.html', {'user': user, 'scraps':courseList})


def lecture(request):
    lectureList = Lecture.objects.all()
    user = request.user
    userSet = Users.objects.get(id=user)
    scrap = Scrap.objects.filter(owner=userSet.uid)
    courseList = []
    is_scrap = []

    # Scrap.objects.filter(owner=userSet).delete()

    for lect in lectureList:    # 모든 lecture 돌면서
        if lect.course not in courseList:
            courseList.append(lect.course)
        else:
            continue
        if not scrap.filter(lecture=lect).exists():  # 일단 scrap에 존재도 안함
            Scrap.objects.create(owner=userSet, lecture=lect, adddate=now.strftime('%Y-%m-%d %H:%M:%S'), state=0)
        elif scrap.filter(lecture=lect, state=1):
            is_scrap.append(lect.course)
    return render(request, 'webeye/lecture.html', {'courseList': courseList, 'scrapList': is_scrap})


@login_required
def lecture_mark_toggle(request, course):
    user = request.user
    userSet = Users.objects.get(id=user)
    lect = Lecture.objects.filter(course=course)
    for index, i in enumerate(lect.values()):
        if not Scrap.objects.filter(owner=userSet.uid, lecture=i['lid']).exists():
            Scrap.objects.create(owner=userSet, lecture=lect[index], adddate=now.strftime('%Y-%m-%d %H:%M:%S'), state=1)
    else:
        scrap = Scrap.objects.filter(owner=userSet.uid, lecture__in=lect, )
        for index, i in enumerate(scrap.values()):
            state = i['state']
            if state == 1:
                Scrap.objects.filter(owner=userSet.uid, lecture__in=lect, ).update(state=0)
            else:
                Scrap.objects.filter(owner=userSet.uid, lecture__in=lect, ).update(state=1)
    return redirect('lecture')


def lecture_list(request, course):
    lect_list = Lecture.objects.filter(course=course)
    return render(request, 'webeye/lecture_list.html', {'lecturelist': lect_list})


def to_video(request, lid):
    lect = Lecture.objects.get(lid=lid)
    video_url = lect.url
    return render(request, 'webeye/main.html', {'video_url': video_url})
