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
from difflib import get_close_matches


def detect_text(image_file):
    try:
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

        print(text)
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
        for x in final:
            print(x)
            abc = re.search(r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})',x)
            if 'Date' in x:
                print(x,"////")
                last = final.index(x)
                break
            elif abc:
                last=final.index(x)
        print(final,"////////////////")
        print("                                                    ")
        print(final[:last],"....................................")
        final_address=final[:last]
        print("length of address:",len(final_address))
        final_address=[x for x in final_address if x!='' if 'ELECT' not in x if len(x)>3]
        print("                                                                  ")
        print("final_address:",final_address)

        if len(final_address)>10:
            for x in final_address:
                abc = re.search(r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})',x)
                if abc:
                    date_index=final_address.index(x)
                    #break
                    final_address=final_address[:date_index]
        final_address=[x.rstrip(' ') for x in final_address]
        final_address = [x.lstrip(' ') for x in final_address if len(x)>4]
        elct_index=''
        for x in final_address:
            if 'Electoral' in x:
                elct_index=final_address.index(x)
        if elct_index != '':
            final_address=final_address[:elct_index]
        person_address=' '.join(x for x in final_address)
        #regex = re.compile('(Facsimile signature of|h air Us2018)')
        person_address=re.sub(r'(Facsimile signature of|h air Us2018|Facsimile Signature of)','',str(person_address))
        # print("final_address:",final_address)
        # print("                                                                               ")
        # print("person_address:",person_address)
        # print("                                            ")
        print("deta:",{"person_address":person_address,"date_of_birth":date_of_birth})
        return ({"person_address":person_address,"date_of_birth":date_of_birth,"image_file":image_file})
    except IndexError as e:
        return ({"error":str(e),"image_file":image_file})
    except Exception as e:
        return ({"error":str(e),"image_file":image_file})

address=[]
for root, dirs, files in os.walk("/home/caratred/Downloads/test/voterdeskew"):
         for filename in files:
             abc=detect_text(root+"/"+filename)
             address.append(abc)
print(address)
with open('/home/caratred/voter.txt','w') as f:
    f.write(str(address))

#detect_text("/home/caratred/Downloads/votecard/voter8.JPG")
