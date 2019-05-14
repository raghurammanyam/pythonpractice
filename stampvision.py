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
from cropaadhar import cropaddress
from difflib import get_close_matches
from country_codes import country_with_codes
import dateparser




def extract_text():
    cities=['Ahmedabad','Amritsar','Bagdogra','Bengaluru','Bhubaneswar','Chandigarh','Chennai','Coimbatore','Delhi','Gaya','Goa','Guwahati','Hyderabad','Jaipur',
    'Kochi',
    'Kolkata',
    'Kozhikode',
    'Lucknow',
    'Madurai',
    'Mangaluru',
    'Mumbai',
    'Nagpur',
    'Pune',
    'Thiruvananthapuram',
    'Tiruchirappalli',
    'Varanasi',
    'Visakhapatnam' ,'Cochin'
    'Goa',
    'Mangalore',
    'Mumbai',
    'Chennai']
    images=['/home/caratred/Downloads/e_visa_croped/entries_availed.jpg','/home/caratred/Downloads/e_visa_croped/visa_expiry.jpg','/home/caratred/Downloads/e_visa_croped/port_of_issue.jpg','/home/caratred/Downloads/e_visa_croped/visa_issue.jpg','/home/caratred/Downloads/e_visa_croped/visa_number.jpg']
    def detect_text(image_file):
      
        #service=['eTOURIST VISA','eBUSSINESS VISA','eMEDICAL VISA','eCONFERENCE Visa','eMEDICAL ATTENDANT VISA']
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
        print("..text getted:",text)
        return block
    
    extracted_text=[detect_text(x) for x in images]
    print("extracted_text:",extracted_text)
    abc=re.findall(r'\s(\d{2} \w+ \d{4}|\d{2}\/\d{2}\/\d{4}|\d{2}\-\w+\-\d{4}|\d{2}\-\w+\-\d{2}|\d{2}\-\d{2}\-\d{4}|\d{2} \w+ \d{2}|\d{2}\.\d{2}\.\d{4}|\d{2}\/\d{1}\/\d{4})',text)
    unique_list = list(OrderedDict((element, None) for element in abc))
    print("find_dates:",abc)
    print("list of dates:",unique_list)
    #parsed_expiry=dateparser.parse('06 DAN 2018',settings={'DATE_ORDER': 'DMY'})
    #print("parse_date:",parsed_expiry.date())
    city=[x.upper() for x in cities]
    bun=[]
    for x in extracted_text:
        result = ''.join(i for i in x if not i.isdigit())

        matched_entries=get_close_matches(x,city)
        #print("matched_entries:",matched_entries)
        if len(matched_entries)>=1:
            bun.append(matched_entries[0])
            print("service:",bun)
    print(bun)
    for x in extracted_text:
        for y in city:
            if y in x:
                print("airport:",x)
extract_text()
