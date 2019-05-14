import base64
import requests
import io
import os
import json
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson
import re
import difflib
from werkzeug.utils import secure_filename
import datetime
from datetime import date
from PIL import Image
from pprint import pprint
import cv2
from os.path import join
from collections import defaultdict,OrderedDict
#from cropaadhar import cropaddress
from difflib import get_close_matches


def detect_text(image_file):
    #crop=cropaddress(image_file)
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
    print(block)
    final_list=[]
    # for x in block:
    #     print(x)
    #     if x == 'Name:':
    #         block.remove(x)
    # print("/",block)
    base = re.compile('([a-zA-Z][0-9])')
    data=base.findall(text)
    #print("///: ",text)
    for x in block:
        if 'Sex:' in x:
            gender = x
            if 'M' in gender:
                sex = "Male"
                final_list.append(sex)
            else:
                sex = "Female"
                final_list.append(sex)
        elif 'Date of Birth' in x:
            date_of_birth = x
            reg = re.compile('(\d{2}\/\d{2}\/\d{4})')
            date=reg.findall(date_of_birth)
            date_of_birth = ''.join(date)
            final_list.append(date_of_birth)
        elif 'Age' in x:
            age = x
            reg = re.compile('(\d{2})')
            AGE = reg.findall(age)
            Age = ''.join(AGE)
            final_list.append(Age)
        elif x.startswith(("Address:","Addrew:","Address :")):
            address = x
            ind = block.index(x)
            print(ind)
            final_list.append(x)
            l = len(final_list)
            final_list.insert(l+1,block[ind+1])
            last_element = final_list[-1:]
            print(final_list,"//")
            print("////: ",final_list[-1:])
            print(final_list,"jjjjj")
            if final_list[-1:].isdigit():
                pass
            else:
                final_list.insert(l+2,block[ind+2])
                last_element = final_list[-1:]




    print("//",final_list)

    # for x in block:
    #     if x.startswith(("Name:","NAME :","FATHER'S NAME:","Father's Name:","Elector's Name :","Father's Name :","Father's","Name :","Elector's Name .")):
    #         if ":" in x:
    #             a = re.split(':',x)
    #             print("aaaaa: ",a)
    #             data.append(a[1])
    #         elif ". " in x:
    #             a = re.split('. ',x)
    #             print(a)
    #             data.append(a[1])
    #         else:
    #             data.append(x)
    # print("//////: ",data)
    # json_data = {"voter_id":data[0],"name":data[1],"Father_name":data[2]}
    # print(json_data)

detect_text("/home/caratred/Downloads/votecard/voter58.JPG")
