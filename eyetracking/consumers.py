from glob import glob
import json
from pickle import FALSE
from random import randint
from time import sleep


import matplotlib.pyplot as plt
import json

# from openpyxl import NUMPY
import torch ## pytorch깔아야함 
import cv2 ## opencv-python 깔아야함

from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from torchvision import transforms
import numpy as np

from channels.generic.websocket import WebsocketConsumer

import asyncio 
import time
import os
import subprocess
import datetime

model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet50', pretrained=True)
model.eval()

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
colors = (colors % 255).numpy().astype("uint8")




class WSConsumer(WebsocketConsumer):
    def analysis(self, video_url,currentTime):
        print('currentTime!!!!!!!!!!!!!!')
        if currentTime is not None:
            afterTime = currentTime+1
            currentTime = datetime.datetime.fromtimestamp(currentTime).strftime('%M:%S')
            afterTime = datetime.datetime.fromtimestamp(afterTime).strftime('%M:%S')
            print(currentTime)
            print(afterTime)
            result = subprocess.Popen(['ffmpeg','-ss',currentTime,'-t',afterTime,'-i',video_url,'-r','30','-f','image2','-update','1','-threads','10','-y','test.jpg'],stdout = subprocess.PIPE)

            out,err = result.communicate()
            exitcode = result.returncode
            if exitcode != 0:
                print(exitcode, out.decode('utf8'), err.decode('utf8'))
            else:
                print('Completed')
            print('video1')

        frame = Image.open('test.jpg')
        frame = np.array(frame)
        print(type(frame))

        color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        pil_image=Image.fromarray(color_coverted)

        ## 모델에 넣기 위한 준비 
        input_tensor = preprocess(pil_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            model.to('cuda')

        with torch.no_grad():
            output = model(input_batch)['out'][0]
            output_predictions = output.argmax(0)

        r = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(pil_image.size)
        r.putpalette(colors)

        numpy_image=np.array(r) 
        sum_numpy_image = sum(sum(numpy_image))
        json_image = numpy_image.tolist()
        self.send(json.dumps({'data':json_image}))
        print('video3')

    def mindpoint(self, xprediction, yprediction, data):
        xprediction = int(xprediction)
        yprediction = int(yprediction)
        
        if data is not None:
            data = np.array(data)
            cal_xprediction = xprediction-380 
            cal_yprediction = yprediction-120
            print('xprediction:',xprediction,'yprediction:',yprediction)
            print('cal_xprediction:',cal_xprediction,'yprediction:',cal_yprediction)
            if 0<=cal_xprediction and cal_xprediction+5<480 and 0<=cal_yprediction and cal_yprediction+5<272:
                if sum(sum(data[cal_yprediction:cal_yprediction+5,cal_xprediction:cal_xprediction+5])) == 0:
                    bool_concentrate = True
                else: 
                    bool_concentrate = False
            else:
                bool_concentrate = False
            data = data.tolist()
        else:
            bool_concentrate = False
        print(bool_concentrate)
        self.send(json.dumps({'xprediction':xprediction, 'yprediction':yprediction,'data':data,'bool_concentrate':bool_concentrate}))

    def receive(self, text_data): ## 사용자가 재생버튼을 누르면 해당 비디오의 소스를 찾고 분석 시작 
        text_data_json = json.loads(text_data)
        video_url = text_data_json['video_src'] #프론트 단에서 넘겨온 값을 토대로 소스 추출 
        self.analysis(video_url,text_data_json['currentTime'])
        self.mindpoint(text_data_json['xprediction'],text_data_json['yprediction'],text_data_json['data'])


