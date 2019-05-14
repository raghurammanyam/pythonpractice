import base64
import requests
import io
import os
import json
import re
import difflib
from werkzeug.utils import secure_filename
import datetime
from datetime import date
from pprint import pprint
import cv2
from os.path import join
from collections import defaultdict,OrderedDict
from difflib import get_close_matches


def detect_text(image_file):
    gender_list =['MALE','FEMALE','Male','Female']
    ignore_list=['ELECTION ','ELECTION COMMISSION OF','S NAME','EECTOR PHOTO IDENTITY','ELECTOR',     'IDENTITY CARD','IDENTITY CAR','Date of Birth','s Name','HI FAM','OF INDIA','INDIA ','INDIA PD','s Name', 'Date of Birtta','IDENTITY CARD']

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
    print("....:",block)
    for y in block:
        removesymbol =re.search(r'([a-zA-Z0-9]+)',y)
        if removesymbol is None:
            block.remove(y)
    print("block:",block)

    final_list=[]
    for x in block:
        if x == 'Name:':
            block.remove(x)
    print("/",block)
    base = re.compile('([a-zA-Z]{3}[0-9]{7}|[a-zA-Z]+[0-9]+)')
    data=base.findall(text)

    print("id...data;;",data)
    data = [x for x in data if len(x)>5]
    regex = re.compile('(Age as on|Photo|hoto 10|er a 6|on Pv6|Age as on )')
    data=([regex.sub('', i) for i in data])
    print(data,"data")
    id =''
    if len(data)>=1:
        for x in data:
            if len(x)>=5:
                if 'XXXX' not in x:
                    id = x
                    print("id:",id)
                    break
    else:
        id=''
    print("...:",data)
    sex=''
    for x in block:
        for y in gender_list:
            if y in x:
                sex = y
                print("getting gender:",y)
    noun = re.compile('([a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+|[a-zA-Z]+ [a-zA-Z]+|[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+)')
    name= noun.findall(text)
    print("names:",name)
    for x in ignore_list:
      r = re.compile(x)
      if list(filter(r.match, name)):
          match = list(filter(r.match, name))
          if match[0]:
              listmatch = match[0]
              pop_dob = name.index(listmatch)
              name.pop(pop_dob)
    for y in name:
        if y in ignore_list:
            pop_dob = name.index(y)
            name.pop(pop_dob)
    likes = ['.*ELECTION.* ','.*IIII.*','.* Photo.*','.*COMMISSION .*','.*EPIC.*','.*XIZ.*','.*care.*','.*card.*','.*water.*','.*ELECTION COMMISSION OF.*','.*S NAME.*','.*Age.*','.*Eeron.*','.*EECTOR PHOTO IDENTITY.*','ELECTOR',     '.*IDENTITY CARD.*','.*IDENTITY.*','.*Date of Birth.*','.*s Name.*','.*HI FAM.*','.*OF INDIA.*','.*INDIA.* ','.*INDIA PD.*','.*s Name.*', '.*Date of Birtta.*','.*IDENTITY CARD.*']
    dob_in=re.compile('[0-9]{2}\/[0-9]{2}\/[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}|[0-9]{2}\/[0-9]{2}\/[0-9]+|[a-zA-Z]{2}\/[a-zA-Z]{2}\/[0-9]+')
    date=dob_in.findall(text)
    print(date,"date of birth")
    date_of_birth=''
    if len(date)>=1:
        date_of_birth=date[0]

    for x in likes:
        r = re.compile(x)
        if list(filter(r.match, name)):
            match = list(filter(r.match, name))
            if match[0]:
                listmatch = match[0]
                pop_dob = name.index(listmatch)
                name.pop(pop_dob)
    print("modified:",name)
    person_name=''
    if len(name)>=1:
        person_name=name[0]
    if id!='':
        for x in block:
            abc = re.search(str(id),x)
            if abc:
                index_match = block.index(x)
                print(index_match,"index_match",x)
        after_removeid =block[index_match+1:]
        print(block[index_match+1:],"detec")
        regex = re.compile('([^a-zA-Z0-9-/ ]|\d+|\-|HI FAM|Name |Father|Duplicate|Name:|NAME|EPIC|SERIES|IDENTITY CARD|HUSBAND|S NAME|card|ELECTOR|Elector|s Name|Husband|Smt|FATHER)')
        after_removeid=([regex.sub('', i) for i in after_removeid])
        after_removeid = [x.lstrip(' ') for x in after_removeid if x!='' if x!='  ' if x!='   ' if x!=' ' if len(x)>=4]
        after_removeid = [x.rstrip(' ') for x in after_removeid]
        after_removeid = [x for x in after_removeid if len(x)>4]
        person_name =after_removeid[0]
        print("after_removeid:",after_removeid)

    print(data,"final")
    json_data = {"uid":id,"name":person_name,"sex":sex,"Date_of_birth":date_of_birth}
    print(json_data)
    # print(final_list,"final")
detect_text("/home/caratred/Downloads/votecard/voter67.JPG")
