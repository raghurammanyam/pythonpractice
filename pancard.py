import base64
import requests
import io
import os
import json
import re
from os.path import join
import dateparser
from facedetect import detect_faces


def detect_text(image_file):
    unlike = ['OF INDIA','INCOME TAX DEPARTMENT','Permanent Account Number','s Name','INDIA','OF INDIA','Birth','INCOME TAX DEPARTMENTS']
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
    block=str(text).split('\n')
    bca=re.findall(r'\s([a-zA-Z]{5}\d{4}[a-zA-Z0-9]{1})',text)
    noun = re.compile('([a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+|[a-zA-Z]+ [a-zA-Z]+|[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+)')
    names = noun.findall(text)
    DOB = re.findall(r'\s(\d{2}\/\d{2}\/\d{4})',text)
    names = [x for x in names if x not in unlike]
    face=detect_faces(image_file,bca[0])
    image_string =''
    if os.path.isfile(face) is True:
        with open(face, 'rb') as image:
            image_string = base64.b64encode(image.read()).decode()
   # print(face,"path")
    #print(names,"/////////////////////////////")
    #print("dateof birth:",DOB)
    parsed_birth=str(dateparser.parse(DOB[0],settings={'DATE_ORDER': 'DMY'}).date())
    print(parsed_birth,"///////////////////////////////")
    details = {"name":names[0],"father_name":names[1],"pan_no":bca[0],"date_of_birth":parsed_birth}
    print(details,"details")
           
detect_text('/home/caratred/Downloads/ram/9.jpg')