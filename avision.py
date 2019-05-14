import base64
import requests
import io
import os
import json
import re
from werkzeug.utils import secure_filename
import datetime
from datetime import date
from PIL import Image
from pprint import pprint
import cv2
from os.path import join
from collections import defaultdict,OrderedDict






def detect_text():
    images=['/home/caratred/adhar/Webcam/21.jpg','/home/caratred/adhar/Webcam/23.jpg','/home/caratred/adhar/Webcam/22.jpg','/home/caratred/adhar/Webcam/24.jpg','/home/caratred/adhar/Webcam/25.jpg']
    def extract(image_file):
        remove=['Name','Valid To','Date of issue']
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
                }],
                "imageContext":{
                "languageHints":["en-t-iO-handwrit"]
                }
            }]
        }
        response = requests.post(url, headers=header, json=body).json()
        text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
        block=str(text).split('\n')
        block=[x for x in block if x!='' ]
        return block
    extracted_text=[extract(x) for x in images]
    offence=[y for x in extracted_text for y in x]
    print("extracted_text:",offence)
    if 'Year of Birth:' in offence[2]:

        date_of_birth=offence[2].lstrip('Year of Birth: ')
    elif 'DOB:' in offence[2]:
        date_of_birth=offence[2].lstrip('DOB: ')
    gender=re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>|\-', ' ', offence[1])
    address=offence[4:]
    address=[x.lstrip('Address:') for x in address]
    address=[x for x in address if x!='']
    data={"name":offence[0],"gender":gender,"date_of_birth":date_of_birth,"uid":offence[3],"address":address}
    print("data:",data)
    return offence

detect_text()
