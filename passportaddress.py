import base64
import requests
import io
import os
import json
import re
from werkzeug.utils import secure_filename
import datetime
from datetime import date
from difflib import get_close_matches
import cv2
from os.path import join
import dateparser


def detect_text(image_file):
    
    with open(image_file, 'rb') as image:
         base64_image = base64.b64encode(image.read()).decode()
    url = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAOztXTencncNtoRENa1E3I0jdgTR7IfL0'
    header = {'Content-Type': 'application/json'}
    body = {
        'requests': [{
            'image': {
                'content': base64_image,
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 100,
            }]#,
            #"imageContext":{
            #"languageHints":["en-t-iO-handwrit"]
            #}
        }]
    }  
    response = requests.post(url, headers=header, json=body).json()
    text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
    print("text:",text)
    block=str(text).split('\n')
    print(block,"...........")
    modified_Text=','.join(map(str, block))
    for x in block:
        if 'Address' in x:https://www.khadims.com/storelocator
            abc = block.index(x)
            print(block[abc+1:],"......////")
    #print(modified_Text.startswith(("Address,")),"//////////////////////")
    print("address:",modified_Text)
  
    
    
detect_text('/home/caratred/Downloads/passportbackside/JHANSI VARA KANAKA MAHA LAKSHMI_VUNDRU_407_0.JPG')