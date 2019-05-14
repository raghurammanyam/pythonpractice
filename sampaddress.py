import base64
import requests
import io
import os
import json
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson
import re
from werkzeug.utils import secure_filename
import datetime
from datetime import date
from PIL import Image
from pprint import pprint
import cv2
from os.path import join
from collections import defaultdict,OrderedDict
from difflib import get_close_matches


def detect_text(image_file):
    try:
        final_address = []
        unlike=['UNIQUE IDENTIFICATION AUTHORITY','OF INDIA','Identification','Bengaluru-560001','-500001','500001','Bengaluru-580001','560001',' WWW','WWW','-560001','-560101','560101','uidai','Aam Admi ka','VvV','he','uldai','uldal','govin','www','A Unique Identification','Www','in','gov','of India','uidai','INDIA','India','www','I','1B 1ST','MERI PEHACHAN','1E 1B','MERA AADHAAR','Unique Identification Authority','of India','UNQUE IDENTIFICATION AUTHORITY','1800 180 1947','1800180 1947','Admi ka Adhikar','w','ww','S','s','1800 180 17','WWW','dai','uidai','Address','1809 180 1947','help','AADHAAR','160 160 1947','Aadhaar','180 18167','Aadhaar-Aam Admi ka Adhikar','gov in','1947','MERA AADHAAR MERI PEHACHAN','38059606 3964','8587 1936 9174']
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
        #print(text)
        for x in block:
            if 'Address' in x:
                abc=block.index(x)
        #        print(abc)
        address=block[abc:]
        #print(address,"before")
        regex = re.compile('([^a-zA-Z0-9-/ ]|Address|No|www|o  |uidai)')
        cannot=([regex.sub('', i) for i in address])
       # print(cannot,"///after")
        #cannot = [x for x in cannot if len(x)>2 if 'No' not in x if 'o  ' not in x if 'www' not in x if 'Address' not in x]
        cannot = [x for x in cannot if x not in unlike]
        unique_list = list(OrderedDict((element, None) for element in cannot))
        for x in unique_list:
            abc =x.lstrip('  ')
            abc  =x.lstrip(' -')
            abc =x.lstrip(' ')
            final_address.append(abc)
        for x in final_address:
            match = re.compile('(govin|ligovin|help)')
            abc = match.search(x)
            if abc:
                index_match = final_address.index(x)
                final_address.remove(x)
        for x in final_address:
            pin = re.search('([0-9]{6})',x)
            if pin:
                ind = final_address.index(x)
                final_address=final_address[:ind+1]
        #print("..........................................................................................")
        #print(final_address[:ind+1],'llllllllllllllllllllllllllllllllllllllllll')
        #print("                                                                                         ")
        #print("////////////////////////////////////////////////////////////////////////////////////////////")
        abc = ' '.join(x for x in final_address)
        final = abc.split()
        final_address= list(OrderedDict((element, None) for element in final))

        #print(final,"//////////////////////////////")
        #print("                                                                        ")
       # print("final_address:",final_address)
        person_address=' '.join(x for x in final_address)
        #print(person_address)
        #print("                                                        ")
        pin_code = re.findall('([0-9]{6})',person_address)
        for x in final_address:
            abc=re.search('([0-9]{6})',x
            if abc:
                final_address.remove(x)
        final_address.append(pin_code[0])
        person_address=' '.join(x for x in final_address)
        print("person_address:",person_address)
        return {"person_address":person_address,"image_file":image_file}
    except IndexError as e:
        return ({"error":str(e),"image_file":image_file})
    except Exception as e:
        return ({"error":str(e),"image_file":image_file})


#    print(abc,"/////,.,,,,,,,,")
    # print(cannot)
    # print(unique_list)
    # print(final_address)
#detect_text('/home/caratred/adhar/Webcam/2019-02-06-125645.jpg')
#detect_text('/home/caratred/Desktop/aadhar.jpg')
#detect_text('/home/caratred/Downloads/aadhaarcard/images/amit_Shukla_242_0.JPG')
address=[]
for root, dirs, files in os.walk("/home/caratred/Downloads/test/aadhardeskew"):
         for filename in files:
             abc=detect_text(root+"/"+filename)
             address.append(abc)
print(address)
with open('/home/caratred/address.txt','w') as f:
    f.write(str(address))
