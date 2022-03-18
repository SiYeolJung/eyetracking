import json
from random import randint
from time import sleep


import matplotlib.pyplot as plt
import json
import torch ## pytorch깔아야함 
import cv2 ## opencv-python 깔아야함

from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from torchvision import transforms
import numpy as np

from channels.generic.websocket import WebsocketConsumer

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
    def receive(self, text_data): ## 사용자가 재생버튼을 누르면 해당 비디오의 소스를 찾고 분석 시작 
        text_data_json = json.loads(text_data)
        video_url = text_data_json['video_src'] #프론트 단에서 넘겨온 값을 토대로 소스 추출 
        cap = cv2.VideoCapture(video_url)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        while (cap.isOpened):
            ret, frame = cap.read()
            ## convert from openCV2 to PIL
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
            self.send(json.dumps({'message':int(sum_numpy_image)}))




    # def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['param']
        # print('Message:',message)
        # self.send(json.dumps({
        #     'type':'chat',
        #     'message':message 
        # }))


    # def connect(self):
    #     self.accept()
    #     self.send(json.dumps({
    #         'type': 'connection_established',
    #         'message':'You are now connected'
    #     }))
    #     #for i in range(1000):
    #     #    self.send(json.dumps({'message':randint(1,100)}))
    #     #    sleep(1)
        
    #     ## 비디오가 정상적으로 열렸는지 확인
    #     while (cap.isOpened):
    #         ret, frame = cap.read()
    #     ## convert from openCV2 to PIL
    #         color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    #         pil_image=Image.fromarray(color_coverted)

    #     ## 모델에 넣기 위한 준비 
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
    #         self.send(json.dumps({'message':int(sum_numpy_image)}))


