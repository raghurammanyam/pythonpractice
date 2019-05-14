import base64
import requests
import io
import os
#from google.cloud import vision
#from google.cloud.vision import types
import pandas as pd
import csv
import json
#from google.protobuf.json_format import MessageToJson
import re
#import mrz
import datetime
from PIL import Image
import PIL.ImageOps
import pycountry
from difflib import get_close_matches
import base64
#from id import detect_faces
import requests
import io
import os
import json
#from google.cloud import vision
#from google.cloud.vision import types
#from google.protobuf.json_format import MessageToJson
import re
from werkzeug.utils import secure_filename
import datetime
from datetime import date
from mrz.base.countries_ops import is_code
from mrz.checker.td3 import TD3CodeChecker
from PIL import Image
from pprint import pprint
from difflib import get_close_matches
import tempfile
import cv2
from os.path import join
import pycountry
import csv
import pandas as pd
import codecs
import pandas as pd
import xlrd as xl
from pandas import ExcelWriter
from pandas import ExcelFile
from xlrd import open_workbook
from collections import defaultdict
import xlrd
from country_codes import country_with_codes

s=[]
c=[]
country_code_list=[]
d = {}
for root, dirs, files in os.walk("/home/caratred/copy/passports"):
    for filename in files:
        print("===============",filename)

        def detect_text():
            countries_names=[]
            country_codes=[]
            official_names=[]
            full_length=[]
            loss = []
            with open(root+"/"+filename, 'rb') as image:
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
                    #"imageContext": {
                    #"languageHints": ["en-t-i0-handwrit"]
                    #}

                }]
            }

            response = requests.post(url, headers=header, json=body).json()
            text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
            list_of_countries=list(pycountry.countries)
            #print(list_of_countries)

            match = re.search(r'\d{2}/\d{2}/\d{4}', text)
            #print("matched date:",match)
            newlist = re.findall(r'-?\d+\.?\d*', text)
            block=str(text).split('\n')

            offence=[]
            #print("blocks data:",block[::-2])
            print("last two lines of passport:",block[::-1])
            for x in block[::-1]:
                if (len(x)>=25):
                    full_length.append(x)
            print("full_length:",full_length)
            appie=block[::-1]
            ca=re.sub(r'\s+', '',str(appie[2]))
            loss.append(ca)
            a=re.sub(r'\s+', '',str(appie[1]))
            #print("replaced data:",a)
            loss.append(a)
            mine=re.sub(r'\s+', '',str(full_length[1]))
            offence.append(mine)
            dug=re.sub(r'\s+', '',str(full_length[0]))
            offence.append(dug)
            #print(tuple(loss))
            #print("appie data:",str(appie[2]),str(appie[1]))
            #print(len(ca),len(a))
            first=loss[0]
            second =loss[1]
            #first=offence[0]
            #second=offence[1]
            length=(len(ca)+len(a))
            #print("length of mrz code:",length)
            if(first[0]=='P'):
                passport_type=('\n'.join(tuple(loss)))
            #    print("datafh:",passport_type)
                mrz_td3 = passport_type
                type=first[0]
                #print("type:",type)
                country_code=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', first[2:5])

                for key,value in country_with_codes.items():
                    #print(key,value)
                    luck=country_code.strip(' ')

                    if (key==luck):
                        print("===============",key,value)

                fullname_with_symbols=first[5:45]
                #print("kkk",pic)
                dan =fullname_with_symbols.strip('<')
                hat=dan.split('<<')
                surname=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', hat[0])
                if (len(hat)==2):
                    mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', hat[1])
                    givenname=mrx
                else:
                    givenname = ''
                    #print("given_name:",givenname)
                document_no=second[0:9]
                passport_no=re.sub(r'[^\w]', ' ',document_no)
                #print("passport_number:",passport_no)
                nationality=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', second[10:13])
                #print("nationality:",nationality)
                birthdate=second[13:19]
                date_of_birth = '/'.join([birthdate[:2],birthdate[2:4],birthdate[4:]])
                #print("date of birth:",date_of_birth)
                abc=re.findall(r'\s([0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+ \d{2}|\d{2} \w+/\w+ \d{2}|\d{2} \w+ \w+ \d{2}|\d{2} \w \/  \w+ \d{2})',text)
                print("date of birth:",abc)
                Date_of_issue=abc[1]
                sex=second[20]
                #print("sex:",sex)
                expiry_date=second[21:27]
                date_of_expiry='/'.join([expiry_date[:2],expiry_date[2:4],expiry_date[4:]])
                data={
                "Passport_Document_Type":type,
                "country_code":country_code,
                "FamilyName":surname,
                "Given_Name":givenname,
                "Passport_Document_No":passport_no,
                "Nationality":nationality,
                "Date_of_Birth":date_of_birth,
                "Gender":sex,
                "Date_of_issue":Date_of_issue,
                "Date_of_Expiry":date_of_expiry
                }
                print(data)
                with open('/home/caratred/copy/new_csv/'+ filename +'.csv', 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in data.items():
                        writer.writerow([key, value])
                return data
            elif(first[0]=='V'):
                #if(length==88):
                act=('\n'.join(tuple(loss)))
                print("datafh:",act)
                #print(MRVACodeChecker(act))
                type=first[0]
                print("document type:",type)
                print("issued state or country:",first[1])
                types_of_visas = ['B-2','B-3','B-1X','B-1','E-1','MEDX','T-1','T- 1','EMPLOYMENT','T','U','B','X-ENTRY','E','E-3','x','TOURIST']
                for x in block[::-1]:

                    for y in x:
                        #print("cols:",get_close_matches(y,types_of_visas))
                        if x in types_of_visas:
                            print("type of visa:",x)
                entries=['MULTIPLE','SINGLE','DOUBLE']
                entry=' '
                for y in block[::-1]:
                    a=get_close_matches(y,entries)
                    print(a)
                    if len(a)==1:
                        entry=a[0]
                        print("no of entries:",a[0])
                    #elif y in entries:
                    #    print("no of entries:",y)
                if (first[1].isalpha()):
                    abc=re.findall(r'\s([0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+/\w+ \d{4} \w+)',text)
                    print("date of issue:",abc,first[1])
                    great = min(abc[0][6:10], abc[1][6:10])
                    for x in abc:
                        if great in x:
                            Date_of_issue=x
                            break
                            print("great value:",x)
                elif (first[1]=='<'):
                    abc=re.findall(r'\s([0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+/\w+ \d{4} \w+)',text)
                    if (len(abc)==2):
                        print("date of issue:",abc[1])
                        Date_of_issue = abc[1]
                    else:
                        Date_of_issue = abc[0]

                issuingcountry=first[2:5]
                print("issuing country :",issuingcountry)
                ad=(first[5:]).strip('<')
                bc=ad.split('<<')
                surname=bc[0]
                print("sur_name:",surname)
                givenname=bc[1]
                print("first_name:",givenname)
                print("name of the person:",first[5:])
                visa_number=second[0:9]
                print("visa_number:",visa_number)
                nationality=second[10:13]
                print("nationality:",nationality)
                birthdate = second[13:19]
                print(birthdate)
                date_of_birth = '/'.join([birthdate[:2],birthdate[2:4],birthdate[4:]])
                print("date of birth:",date_of_birth)
                sex=second[20]
                print("sex:",sex)
                expiry_date=second[21:27]
                date_of_expiry='/'.join([expiry_date[:2],expiry_date[2:4],expiry_date[4:]])
                print("expiry_date:",date_of_expiry)
                optional_data=second[28:]
                print("optional_data:",optional_data)
                data={"type":type,"issued_country":issuingcountry,"visa_no_of_entries":entry,"sur_name":surname,"given_name":givenname,"Date_of_issue":Date_of_issue,"visa_no":visa_number,"nationality":nationality,"date_of_birth":date_of_birth,"gender":sex,"visa_expirydate":date_of_expiry}
                print("person_visa_details:",data)
                with open('/home/caratred/copy/new_csv/'+ filename +'.csv', 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in data.items():
                        writer.writerow([key, value])
                return data
        detect_text()


        print("=============================================================================================================")
'''
for con in country_code_list:
    if con not in d:
        d[con]=1
    else:
        d[con] +=1
print(country_code_list)
print(d)
'''
