import base64
import requests
import io
import os
import json
# from google.cloud import vision
# from google.cloud.vision import types
# from google.protobuf.json_format import MessageToJson
import re
# from werkzeug.utils import secure_filename
import datetime
from datetime import date
from PIL import Image
from pprint import pprint
import cv2
from os.path import join
from collections import defaultdict,OrderedDict
#from visaqr import qr_scan
from id import detect_faces
# from cropaadhar import cropaddress
from difflib import get_close_matches
from country_codes import country_with_codes





def detect_text(image_file):

    service=['eTOURIST VISA','eBUSSINESS VISA','eMEDICAL VISA','eCONFERENCE Visa','eMEDICAL ATTENDANT VISA']
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
    print("fulltext:",text)
    #print("list of visa entities:",block)
    entries=['MULTIPLE','SINGLE','DOUBLE','Double','Single','Multiple']
    entry=' '
    for y in block:
            result = ''.join(i for i in y if not i.isdigit())
            matched_entries=get_close_matches(result,entries)

            if len(matched_entries)==1:
                entry=matched_entries[0]
                #print("entry:",entry)
    details = {}
    
    get=country_with_codes.values()
    get=[x.upper() for x in list(get)]
    #print(".....:",get)
    nation=[]
    for x in block:
        if x in get:
            print("country:",x)
        result = ''.join(i for i in x if not i.isdigit())
        matched_entries=get_close_matches(x,get)
        # print("matched_entries:",matched_entries)
        if len(matched_entries)>=1:
            nation.append(matched_entries[0])
    nationality = ''
    if len(nation)>0:
        nationality=nation[0]
    type_visa=[]
    for x in block:
        result = ''.join(i for i in x if not i.isdigit())
        matched_entries=get_close_matches(x,service)
       # print("matched_entries:",matched_entries)
       
        if len(matched_entries)>=1:
            type_visa.append(matched_entries[0])
    visa_type=''
    print(bun)
    if len(bun)>=1:
        visa_type =type_visa[0]
            #print("service:",bun)
    #print(bun[1])
    details['visa_Type']=visa_type
    details['Nationality']= nationality
    details['Visa_No_Of_Enteries']=entry
    details['Issued_country']='INDIA'
    details['Document_Type']='e-VISA'
    
    print("details:",details)
    #return ad
detect_text('/home/raghu/Downloads/e-visa1.jpg')
