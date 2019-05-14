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
    images=['/home/caratred/adhar/images/no.JPG','/home/caratred/adhar/images/name.JPG','/home/caratred/adhar/images/address.JPG','/home/caratred/adhar/images/issue.JPG','/home/caratred/adhar/images/expiry2.JPG']
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
        block=[x for x in block if x!='' if x not in remove]
        print("fulltext:",text)
        return block
    extracted_text=[extract(x) for x in images]
    print("extracted_text:",extracted_text)
    extracted_text = [y for x in extracted_text for y in x]
    print("extracted_text:",extracted_text)


detect_text()
