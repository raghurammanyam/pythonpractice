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






def detect_text(image_file):
    gender_list =['MALE','FEMALE','Male','Female']
    remove=['GOVERNMENT OF INDIA','Government of India','Year of Birth','/ Male']
    dot=['Year of Birth','of Birth','/ Male','/ MALE','Year of Birh','OF INDIA','/ DOB','Year of Birth','/ Year','/ Female']
    blob=[]
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
    abc=[str(x) for x in block ]
    detail=[]
    base=re.findall(r'\s(\d{12}|\d{5} \d{8}|\d{4} \d{4} \d{4}|\d{2}\/\d{2}\/\d{4}|\d{8} \d{4}|\d{2}\/\d{2}\/\d{3}|\d{4}|\d{2}\/\d{2}\/\d{4}|\d+ \d{8}|[0-9][0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]|\w+ \w+ \w+|\w+\: [0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]|\w+\: [0-9][0-9][0-9][0-9]|\d{8}\ \d{4}|\d{4}\ \d{8}|[0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9]|\/ \w+|\w+ \w+|\w+ \: \d{2}/\d{2}/\d{4}|\w+ \w+ \w+ \ \d{4})',text)
    print("last two lines of aadhar:",base[::-1])
    hexa = [y for y in base if y!='Scanned by CamScanner']
    print("hexa data:",hexa)
    hexa = [ x for x in hexa if x not in remove]
    print("hexa:",hexa)
    block=[x.lstrip('/') for x in block ]
    print("sdfsdf:",block)
    gender_list =['MALE','FEMALE','Male','Female']
    for x in block:
        for y in gender_list:
            if y in x:
                gender = y
                print("getting gender:",y)
    da_find=re.compile('([0-9]+ [0-9]+ [0-9]+|[0-9]+ [0-9]+|[0-9]{12})')
    number=da_find.findall(text)
    print("number:",number)
    na_find=re.compile('([a-zA-Z]+ [a-zA-Z]+)')
    noun=na_find.findall(text)
    print("name:",noun)
    likes=[".*GOVERNMENT*.",".*Government*."]
    for x in likes:
       r = re.compile(x)
       if list(filter(r.match, noun)):
           match = list(filter(r.match, noun))
           if match[0]:
               listmatch = match[0]
               pop_dob = noun.index(listmatch)
               noun.pop(pop_dob)

    print("full_data:",noun)
    dob_in=re.compile('[0-9]{4}|[0-9]{2}\/[0-9]{2}\/[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}')
    date=dob_in.findall(text)
    print("date_of_birth:",date)

    hexa = [x for x in hexa if 'Father' not in x]
    x=hexa[::-1]
    print("data:",x)
    x.insert(1,gender)
    print("xdv:",x)
    x= [ x for x in x if x not in dot]
    regex = re.compile('([^a-zA-Z0-9-/ ])')
    x=([regex.sub('', i) for i in x])
    x=[y for y in x if y !=' ']
    print("after before:",x)
    uid = number[0]

    sex = gender

    print("dfg:",sex)
    name=x[3]
    birth = x[2]
    date_of_birth = birth.lstrip('of Birth: ')
    date_of_birth = date_of_birth.lstrip('DOB:')
    data={'name':name, "gender":sex, "uid":uid,"date_of_birth":date_of_birth,"year_of_birth":yob}
    print("details:",data)
    return data

detect_text('/home/caratred/Downloads/aadhaarcard/images/rajesh_iyer_421.JPG')
