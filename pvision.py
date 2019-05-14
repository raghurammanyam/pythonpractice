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
from abctext import detect_api
import dateparser


def detect_text():
    images=['/home/caratred/Downloads/drivers/mrz2.jpeg','/home/caratred/Downloads/drivers/issue2.jpg.jpeg','/home/caratred/Downloads/drivers/place23.jpeg']
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
        abc=[]
        response = requests.post(url, headers=header, json=body).json()
        text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
        block=str(text).split('\n')


        block=[x for x in block if x!='' ]
        return block
    extracted_text=[extract(x) for x in images]
    offence=[y for x in extracted_text for y in x]
    abc=detect_api(offence)
    print("sdjfnsd:",abc)
    return abc
detect_text()
