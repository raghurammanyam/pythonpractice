import base64
import requests
import io
import os
import json
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
#import pycountry
import csv
import pandas as pd
import codecs
import pandas as pd
#import xlrd as xl
# from pandas import ExcelWriter
# from pandas import ExcelFile
# from xlrd import open_workbook
from collections import defaultdict
#import xlrd
from country_codes import country_with_codes
#from date_extractor import extract_dates
#import datefinder
import dateparser
#import moment
from rotate import autorotate





loss=[]
hall=[]
tune=[]

def detect_text(image_file):
    #auto=autorotate(image_file)

    countries_names=[]
    country_codes=[]
    official_names=[]
    #image = Image.open(image_file)
    #greyscale_image = image.convert('L')
    #greyscale_image.save('/home/caratred/image/greyscale_image.jpg')
    #img = cv2.GaussianBlur(image_file, (15,15), 0)
    #img.save('/home/caratred/image/greyscale_image.jpg')
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
                'maxResults': 100,
            }],
            "imageContext":{
            "languageHints":["en-t-iO-handwrit"]
            }
        }]
    }

    face_body = {
        'requests': [{
            'image': {
                'content': base64_image,
            },
            'features': [{
                'type': 'FACE_DETECTION',
                'maxResults': 10,
            }]
            #"imageContext":{
            #"languageHints":["en-t-iO-handwrit"]
            #}
        }]
    }
    respone_face = requests.post(url, headers=header, json=face_body).json()
    #print("sjdfbgjdfbsgkvdfk",respone_face)
    response = requests.post(url, headers=header, json=body).json()
    #print(response)
    #print ("response",response)
    text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
    #for x in text:

    #print(h)
    print ("kdfjgn:",text)
    #print(list(pycountry.countries))
    dates = extract_dates(text)
    print("date_extractor:",dates)
    #matches = list(datefinder.find_dates(text))
    #print("matches:",matches)
    list_of_countries=list(pycountry.countries)
    #print(list_of_countries)
    for y in list_of_countries:

        #print("country names:",y.__dict__['_fields']['official_name'])
        countries_names.append(y.__dict__['_fields']['name'].upper())
        country_codes.append(y.__dict__['_fields']['alpha_3'].upper())
    #print(countries_names)

    for y in list_of_countries:
        if 'official_name' in y.__dict__['_fields'].keys():
            #print("country names:",y.__dict__['_fields']['official_name'])
            official_names.append(y.__dict__['_fields']['official_name'].upper())

    #print(countries_names)
    #print("codes",country_codes)
    #print("----------------",official_names)
    #print(dict(zip(country_codes,countries_names)))
    #country_with_codes = dict(zip(country_codes,countries_names))
    match = re.search(r'\d{2}/\d{2}/\d{4}', text)
    #print("matched date:",match)
    newlist = re.findall(r'-?\d+\.?\d*', text)
    #print("mgnd:",newlist)
    #email = re.compile('\w+@\w+\.[a-z]{3}')
    #email = re.compile('\d{2} \w+/\w+ \d{4}')
    #get = email.findall(text)
    #print("dfgvsd:",get)

    block=str(text).split('\n')
    #for x in block[::-1]:
        #print(x)
        #print("closed matches:",get_close_matches(x,country_codes))
        #if x in countries_names:
    #        print("/////////////////////////////////////////////")
    #        print("country_name:",x)
        #elif x in official_names:
    #        print(",,,,,,,,,,,,,,,,: ",x)
        #elif get_close_matches(x,countries_names):
        #    print("ggggggggggggggggggggggg",get_close_matches(x,countries_names))


    #print("blocks data:",block[::-2])
    print("last two lines of passport:",block[::-1])
    appie=block[::-1]
    ca=re.sub(r'\s+', '',str(appie[2]))
    loss.append(ca)
    a=re.sub(r'\s+', '',str(appie[1]))
    #print("replaced data:",a)
    loss.append(a)
    #print(tuple(loss))
    #print("appie data:",str(appie[2]),str(appie[1]))
    #print(len(ca),len(a))
    first=loss[0]
    second =loss[1]
    length=(len(ca)+len(a))
    #print("length of mrz code:",length)
    if(first[0]=='P'):
        workbook = xlrd.open_workbook('/home/caratred/test.xls')
        worksheet = workbook.sheet_by_name("Sheet1")
        names = (name.value for name in worksheet.col(0))
        ages = ((age.value) for age in worksheet.col(1))
        data_code = dict(zip(ages, names))

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



        #print("country_code:",country_code)
        #for key,value in country_with_codes.items():
        #    if (key==country_code):
        #       print("===\\\\==",value)
        #       county_name = value
        #for x in block[::-1]:
            #print(x)
            #print("closed matches:",get_close_matches(x,country_codes))
            #if x in countries_names:
    #            print("/////////////////////////////////////////////")
    #            print("country_name:",x)
            #elif x in official_names:
    #            print(",,,,,,,,,,,,,,,,: ",x)
            #else:
    #            print("...............",county_name)
            #    break"""
        fullname_with_symbols=first[5:45]
        #print("kkk",pic)
        dan =fullname_with_symbols.strip('<')
        hat=dan.split('<<')
        #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",hat,len(hat))
        surname=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', hat[0])
        #print("surname:",surname)
        if (len(hat)==2):
            mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', hat[1])
            givenname=mrx
            #print("given name:",givenname)
        else:
            givenname = ''
            #print("given_name:",givenname)
        document_no=second[0:9]
        passport_no=re.sub(r'[^\w]', ' ',document_no)
        #print("passport_number:",passport_no)
        nationality=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', second[10:13])
        #print("nationality:",nationality)
        birthdate=second[13:19]
        birth_joindate = '/'.join([birthdate[:2],birthdate[2:4],birthdate[4:]])
        parsed_birth=dateparser.parse(birth_joindate,settings={'DATE_ORDER': 'YMD'})
        print(parsed_birth)
        if parsed_birth==None:
            date_of_birth =''
        else:
            date_of_birth = str((parsed_birth).date())
            year = date_of_birth[0:4]

            present_date=datetime.datetime.now()
            present_year=present_date.year
            if str(present_year)<year:
                two=date_of_birth[0:2]
                remain=date_of_birth[2:]
                full=two.replace(str(20),str(19))
                date_of_birth=full+remain
        #print("date of birth:",date_of_birth)
        abc=re.findall(r'\s([0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+ \d{2}|\d{2} \w+/\w+ \d{2}|\d{2} \w+ \w+ \d{2})',text)
       # print("date of birth:",abc)
        #Date_of_issue=abc[1]
        static  = [' ','.','/','-']

        #m = moment.date('03 JAN/JAN 78', '%Y-%m-%d')
        #print("moment_data:",m)
        dates=[]
        for x in abc:
            for y in static:
                if y in (x):
                    print("date:",x)
                    if len(x)>7:
                        parse_date=dateparser.parse(x)
                        print("parser_data:",parse_date)
                        dates.append(x)
        res = []
        [res.append(x) for x in dates if x not in res]
        #print("datesbu:",res)
        parsed_issue=dateparser.parse(res[1],settings={'DATE_ORDER': 'DMY'})
       # print("parsed_issue:",parsed_issue)
        if parsed_issue==None:
            Date_of_issue=' '
        else:
            issue_join=str((parsed_issue).date())
            Date_of_issue=issue_join


        sex=second[20]
        #print("sex:",sex)
        expiry_date=second[21:27]
        expiry_joindate='/'.join([expiry_date[:2],expiry_date[2:4],expiry_date[4:]])
        parsed_expiry=dateparser.parse(expiry_joindate,settings={'DATE_ORDER': 'YMD'})
        if parsed_expiry==None:
            date_of_expiry =' '
        else:
            date_of_expiry = str((parsed_expiry).date())
        if Date_of_issue == date_of_expiry or Date_of_issue == date_of_birth:
            Date_of_issue= ' '



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
        pprint(data)
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
            print("date of issue:",abc[1])
            Date_of_issue = abc[1]
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
        return data
#detect_text('/home/caratred/Downloads/drivers/1234.jpg')
detect_text('/home/raghu/Downloads/Down-Payment/Florida.pdf')
#print("mrz data:",tuple(loss))
"""first=loss[0]
second =loss[1]
act=('\n'.join(tuple(loss)))
print("datafh:",act)
mrz_td3 = act

td3_check = TD3CodeChecker(act, check_expiry=True)

print("passport reader:",td3_check.mrz_code)
type=first[0]
print("type:",type)
country_code=first[2:5]
print("country_code:",country_code)
pic=first[5:45]
print("kkk",pic)
dan =pic.strip('<')
hat=dan.split('<<')
surname=hat[0]
print("surname:",surname)
mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', '', first[5:45])
givenname=hat[1]
print("given name:",givenname)
passport_no=second[0:9]
print("passport_number:",passport_no)
nationality=second[10:13]
print("nationality:",nationality)
birthdate=second[13:19]
print("date of birth:",birthdate)
sex=second[20]
print("sex:",sex)
expiry_date=second[21:27]
print("expiry_date:",expiry_date)
#canon=detect_faces('/home/caratred/image/passports/China.png')
#print("imagepath of face:",canon)
data={"type":type,"country_code":country_code,"surname":surname,"givenname":givenname,"passportnumber":passport_no,"nationality":nationality,"date of birth":birthdate,"sex":sex,"expirydate":expiry_date}
print("person_passport_details:",data)

if (td3_check==True):
    print("type:",first[0])
    print("country_code:",first[2:5])
    mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', '', first[5:45])

    #print("ignm:",mrx)
    print("full name:",mrx)
    print("passport_number:",second[0:10])
    print("date of birth:",second[13:19])
    print("sex:",second[20])
    print("'%s' is code: %s" % (td3_check._country, str(is_code("TWN"))))
else:
    print("Falses:", td3_check.report_falses)
    print("Warnings:", td3_check.report_warnings)"""

"""
if not td3_check:
    print("Falses:", td3_check.report_falses)
    print("Warnings:", td3_check.report_warnings)
print("type:",first[0])
print("country_code:",first[2:5])
mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', '', first[5:45])

#print("ignm:",mrx)
print("full name:",mrx)
print("passport_number:",second[0:10])
print("date of birth:",second[13:19])
print("sex:",second[20])


print("'%s' is code: %s" % (td3_check._country, str(is_code("TWN"))))"""
