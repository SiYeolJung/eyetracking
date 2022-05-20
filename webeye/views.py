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
from .models import Profile, Lecture
# Create your views here.

def basic(request):
    return render(request,'webeye/index.html')

def video(request):
    return render(request,'webeye/main.html')

# def classifyvideo(request):
#     jsonObject = json.loads(request.body)
#     model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet50', pretrained=True)
#     model.eval()

#     preprocess = transforms.Compose([
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#     ])

#     palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
#     colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
#     colors = (colors % 255).numpy().astype("uint8")
    
#     cap = cv2.VideoCapture(jsonObject.get('src')) ## 영상 캡처할 url 넣기 

#     width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#     height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

#     ## 비디오가 정상적으로 열렸는지 확인
#     while (cap.isOpened):
#         ret, frame = cap.read()
#         ## convert from openCV2 to PIL
#         color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
#         pil_image=Image.fromarray(color_coverted)

#         ## 모델에 넣기 위한 준비 
#         input_tensor = preprocess(pil_image)
#         input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

#         if torch.cuda.is_available():
#             input_batch = input_batch.to('cuda')
#             model.to('cuda')

#         with torch.no_grad():
#             output = model(input_batch)['out'][0]
#         output_predictions = output.argmax(0)

#         r = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(pil_image.size)
#         r.putpalette(colors)

#         numpy_image=np.array(r) 
#         sum_numpy_image = sum(sum(numpy_image))
        
#         result_classify ={
#             "result" : "sum_numpy_image"
#         }
#         #return JsonResponse(result_classify)
    
#     return render(request,'webeye/main.html') 

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            Profile.objects.create(user=user)
            auth.login(request, user)
            return redirect('/')
        return render(request, 'webeye/signup.html')
    return render(request, 'webeye/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not Profile.objects.filter(user=user):
                Profile.objects.create(user=user)
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
    return render(request, 'webeye/mypage.html', {'user': user})


def myinfo(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    return render(request, 'webeye/myinfo.html', {'user': user})


def lecture(request):
    lecturelist = Lecture.objects.all()
    return render(request, 'webeye/lecture.html', {'lecturelist': lecturelist})


@login_required
def lecture_mark_toggle(request, lecture_id):
    lect = get_object_or_404(Lecture, pk=lecture_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if profile.mark_lecture.filter(id=lecture_id).exists():
        profile.mark_lecture.remove(lect)
        lect.mark_count -= 1
        lect.save()
    else:
        profile.mark_lecture.add(lect)
        lect.mark_count += 1
        lect.save()

    return redirect('lecture')