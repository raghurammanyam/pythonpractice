import base64
from id import detect_faces
import requests
import io
import os
import json
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson
import re
import datetime
from datetime import date
from mrz.base.countries_ops import is_code
from mrz.checker.mrva import MRVACodeChecker
from mrz.checker.mrvb import MRVBCodeChecker
loss=[]
hall=[]
tune=[]

def detect_text(image_file):

    with open(image_file, 'rb') as image:
        base64_image = base64.b64encode(image.read()).decode()
    #print(base64_image)
    url = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAOztXTencncNtoRENa1E3I0jdgTR7IfL0'
    header = {'Content-Type': 'application/json'}
    body = {
        'requests': [{
            'image': {
                'content': base64_image,
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 10,
            }]

        }]
    }
    response = requests.post(url, headers=header, json=body).json()
    print(response)
    #print ("response",response)
    text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
    #for x in text:

    #print(h)
    print (text)
    block=str(text).split('\n')
    #print("blocks data:",block[::-2])
    print("last two lines of passport:",block[::-1])
    appie=block[::-1]
    ca=re.sub(r'\s+', '',str(appie[2]))
    loss.append(ca)
    a=re.sub(r'\s+', '',str(appie[1]))
    print("replaced data:",a)
    loss.append(a)
    print(tuple(loss))
    print("appie data:",str(appie[2]),str(appie[1]))
    print(len(str(appie[2])),len(a))



    return text

detect_text('/home/caratred/image/mrz/docs/images/visas/USA.png')
#print("mrz data:",tuple(loss))
first=loss[0]
second =loss[1]
length=(len(first)+len(second))
print("length_of_mrzcode:",(len(first)+len(second)))

act=('\n'.join(tuple(loss)))
print("datafh:",act)
mrvb = act
#print(MRVACodeChecker(mrvb))
if(length==88):
    print(MRVACodeChecker(act))
    print("document type:",first[0])
    print("issued state or country:",first[1])
    print("issuing country :",first[2:5])
    ad=(first[5:]).strip('<')
    bc=ad.split('<<')
    print("sur_name:",bc[0])
    print("first_name:",bc[1])
    print("name of the person:",first[5:])
    print("visa_number:",second[0:9])
    print("nationality:",second[10:13])
    print("date of birth:",second[13:19])
    birth=int(second[13:19])
    date = datetime.datetime.strptime(birth.group(), '%Y%m%d').date()
    print ("birthdate:",date)
    print("sex:",second[20])
    print("expiry_date:",second[21:27])
    print("optional_data:"[28:])
elif(length==72):
    print(MRVBCodeChecker(act))
    print("document type:",first[0])
    print("issued state or country:",first[1])
    print("issuing country :",first[2:5])
    ad=(first[5:]).strip('<')
    bc=ad.split('<<')
    print("sur_name:",bc[0])
    print("first_name:",bc[1])
    print("name of the person:",first[5:])
    print("visa_number:",second[0:9])
    print("nationality:",second[10:13])
    print("date of birth:",second[13:19])
    print("sex:",second[20])
    print("expiry_date:",second[21:27])
    print("optional_data:"[28:])
