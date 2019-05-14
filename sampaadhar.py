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
from collections import defaultdict
from difflib import get_close_matches
import dateparser





def detect_text(image_file):
    remove=['GOVERNMENT OF INDIA','Government of India','Year of Birth','/ Male','GOVERNMENT OF IND','Nent of India','GOVERMENTER']
    dot=['Year of Birth','of Birth','/ Male','/ MALE','Year of Birh','OF INDIA','/ DOB','Year of Birth','/ Year','/ Female']
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
    print ("kdfjgn:",text)
    yob=''
    block=str(text).split('\n')
    abc=[str(x) for x in block]
    dob_in=re.compile('[0-9]{4}|[0-9]{2}\/[0-9]{2}\/[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}|[0-9]{2}\/[0-9]{2}\/[0-9]+')
    date=dob_in.findall(text)
    date_of_birth = date[0]
    print("date_of_birth:",date)
    for y in date:
        find_date = re.search(r'([0-9]{2}\/[0-9]{2}\/[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}|[0-9]{2}\/[0-9]{2}\/[0-9]+)',y)
        if find_date:
            date_of_birth=y
    parsed_birth=dateparser.parse(date[0],settings={'DATE_ORDER': 'YMD'}).date()
    print(parsed_birth,"parsed_birth")
    gender_list =['MALE','FEMALE','Male','Female']
    gender =''
    for x in block:
        for y in gender_list:
            if y in x:
                gender = y
                print("getting gender:",y)
    da_find=re.compile('([0-9]+ [0-9]+ [0-9]+|[0-9]+ [0-9]+|[0-9]{12})')
    number=da_find.findall(text)
    uid=number[0]
    for x in number:
        find_uid = re.search(r'([0-9]+ [0-9]+ [0-9]+)',x)
        if find_uid:
            uid = x
    print("uid:",number)
    na_find=re.compile('([a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+|[a-zA-Z]+ [a-zA-Z]+|[a-zA-Z]+)')
    noun=na_find.findall(text)
    noun = [x for x in noun if x not in remove]
    person_details={"Date_of_birth":date_of_birth,"sex":gender,"uid":uid,"name":noun[0]}
    return person_details

detect_text('/home/caratred/Downloads/aadhaarcard/images/nupur_roongta_120.JPG')
#detect_text('/home/caratred/adhar/prasoona.jpg')
