import base64
import requests
import io
import os
import json
import re
import difflib
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
    try:
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
            if 'ADDRESS' in x:
                print(x)
                abc=block.index(x)
                print(abc)
            elif 'Address' in x:
                print(x)
                abc=block.index(x)
                print(abc)
            elif 'Addres'  in x:
                print(x)
                abc=block.index(x)
                print(abc)
            elif 'Addre'  in x:
                print(x)
                abc=block.index(x)
                print(abc)
        date_of_birth=''
        for x in block[:abc]:
            find_date = re.compile(r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})')
            date_find = find_date.findall(x)
            if len(date_find)==1:
                date_of_birth=date_find[0]
        final=block[abc:]
        regex = re.compile('([^a-zA-Z0-9-/ ]|Address|Addres|Addre|ADDRESS)')
        final=([regex.sub('', i) for i in final])
        last = ''
        for x in final:
            print(x)
            if 'Date' in x:
                print(x,"////")
                last = final.index(x)
                break
        # print(final,"////////////////")
        # print("                                                    ")
        # print(final[:last],"....................................")
        if last != '':
            final_address=final[:last]
        else:
            add_length=(len(final))//2
            final_address=final[:add_length+5]
        print("length of address:",len(final_address))
        final_address=[x for x in final_address if x!='' if 'ELECT' not in x if len(x)>3]
        # print("                                                                  ")
        # print("final_address:",final_address)
        date_index=''
        if len(final_address)>10:
            for x in final_address:
                abc = re.search(r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})',x)
                if abc:
                    date_index=final_address.index(x)        
                   
        if date_index !='':
            final_address=final_address[:date_index]
        final_address=[x.rstrip(' ') for x in final_address]
        final_address = [x.lstrip(' ') for x in final_address if len(x)>4]
        person_address=' '.join(x for x in final_address)
        print("final_address:",final_address)
        return {"person_address":person_address,"Date_of_birth":date_of_birth,"image":image_file}
    except Exception as e:
        return ({"error":str(e),"image":image_file})
data=[]
for root, dirs, files in os.walk("/home/raghu/Pictures/voterback"):
        for filename in files:
             abc=detect_text(root+"/"+filename)
             data.append(abc)
# #print(address)
with open('/home/raghu/voterbacktest.txt','w') as f:
    f.write(str(data))

# detect_text("/home/caratred/Downloads/votecard/voter58.JPG")
