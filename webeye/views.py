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

now = datetime.datetime.now()
# Create your views here.

def basic(request):
    return render(request,'webeye/index.html')

def video(request):
    return render(request,'webeye/main.html')

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
    return render(request, 'webeye/mypage.html', {'user': user, 'scraps':myScrap})


def myinfo(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    return render(request, 'webeye/myinfo.html', {'user': user})


def lecture(request):
    lectureList =  Lecture.objects.all()
    
    groupList = {}
    for lecture in lectureList:
        if lecture.course in groupList:
            groupList[lecture.course].append({
                'title':lecture.title, 
                'teaches':lecture.teaches,
                'lid':lecture.lid
            })
        else:
            groupList[lecture.course] = [{
                'title':lecture.title, 
                'teaches':lecture.teaches,
                'lid':lecture.lid
            }]

    return render(request, 'webeye/lecture.html', {'lecturelist': groupList})


@login_required
def lecture_mark_toggle(request, lecture_id):
    lect = get_object_or_404(Lecture, pk=lecture_id)
    user = request.user
    userSet = Users.objects.get(id=user)
    lectureSet = Lecture.objects.get(pk=lecture_id)

    if Scrap.objects.filter(owner=userSet.uid, lecture = lecture_id).exists():
        scrap = Scrap.objects.filter(owner=userSet.uid, lecture = lecture_id)
        state = scrap[0].state
        if state == 0:
            scrap.update(state=1)
        else:
            scrap.update(state=0)
    else:
        Scrap.objects.create(owner = userSet, lecture = lectureSet, adddate = now.strftime('%Y-%m-%d %H:%M:%S'), state = 1)

    return redirect('lecture')