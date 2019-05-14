import base64
import requests
import io
import os
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import csv
import json
from google.protobuf.json_format import MessageToJson
import re
import glob
import cv2
import datetime

'''
rootdir = '/home/caratred/copy/passport/'
data_path = os.path.join(rootdir,'*g')
files = glob.glob(data_path)
'''

s=[]
c=[]
for root, dirs, files in os.walk("/home/caratred/copy/passport/"):
    for filename in files:
        x = filename
        def detect_text():
            print("---------------------------------------------------------------------------------------------------------------------------")
            loss=[]
            with open(root+x, 'rb') as image:
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
                    }]#,
                    #"imageContext": {
                    #"languageHints": ["en-t-i0-handwrit"]
                    #}

                }]
            }
            response = requests.post(url, headers=header, json=body).json()
            #print ("response",response)
            text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
            #print("details",text)

            block=str(text).split('\n')
            print("last two lines of passport:",block[::-1])
            appie=block[::-1]
            ca=re.sub(r'\s+', '',str(appie[2]))
            loss.append(ca)
            a=re.sub(r'\s+', '',str(appie[1]))
            print("replaced data:",a)
            loss.append(a)
            print(tuple(loss))
            print("appie data:",ca,a)
            print(len(ca),len(a))
            first=loss[0]
            second =loss[1]
            length=(len(ca)+len(a))
            print("length of mrz code:",length)
            if(first[0]=='P'):
                print("dataloss:",loss)
                act=('\n'.join(tuple(loss)))
                print("datafh:",act)
                #mrz_td3 = act
                #td3_check = TD3CodeChecker(act, check_expiry=True)
                #print("passport reader:",td3_check.mrz_code)
                type=first[0]
                print("type:",type)
                country_code=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', first[2:5])
                print("country_code:",country_code)
                pic=first[5:45]
                print("kkk",pic)
                dan =pic.strip('<')
                hat=dan.split('<<')
                print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",hat)
                surname=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', hat[0])
                print("surname:",surname)
                if (len(hat)==2):
                    mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', hat[1])
                    givenname=mrx
                    print("given name:",givenname)
                else:
                    givenname = ''
                    print("given_name:",givenname)
                document_no=second[0:9]
                passport_no=re.sub(r'[^\w]', ' ',document_no)
                print("passport_number:",passport_no)
                nationality=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', second[10:13])
                print("nationality:",nationality)
                birthdate=second[13:19]
                date_of_birth = '/'.join([birthdate[:2],birthdate[2:4],birthdate[4:]])
                print("date of birth:",date_of_birth)
                sex=second[20]
                print("sex:",sex)
                expiry_date=second[21:27]
                date_of_expiry='/'.join([expiry_date[:2],expiry_date[2:4],expiry_date[4:]])
                print("expiry_date:",date_of_expiry)
                #canon=detect_faces('/home/caratred/image/passports/China.png')
                #print("imagepath of face:",canon)
                data={"Passport_Document_Type":type,"country_code":country_code,"FamilyName":surname,"Given_Name":givenname,"Passport_Document_No":passport_no,"Nationality":nationality,"Date_of_Birth":date_of_birth,"Gender":sex,"Date_of_Expiry":date_of_expiry}
                print("person_passport_details:",data)
                #filename = passport_no
                with open('/home/caratred/image/csv/passport1/'+ x +'.csv', 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in data.items():
                        writer.writerow([key, value])
                return data
            elif(first[0]=='V'):
                if(length==88):
                    act=('\n'.join(tuple(loss)))
                    print("datafh:",act)
                    #print(MRVACodeChecker(act))
                    type=first[0]
                    print("document type:",type)
                    print("issued state or country:",first[1])
                    issuingcountry=first[2:5]
                    print("issuing country :",issuingcountry)
                    ad=(first[5:]).strip('<')
                    bc=ad.split('<<')
                    surname=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', bc[0])
                    print("sur_name:",surname)
                    if (len(hat)==2):
                        mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', bc[1])
                        givenname=mrx
                        print("given name:",givenname)
                    else:
                        givenname = ''
                        print("given_name:",givenname)
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
                    data={"Visa_Type":type,"Issued_country":issuingcountry,"FamilyName":surname,"Given_Name":givenname,"Visa_Number":visa_number,"Nationality":nationality,"Date_of_Birth":date_of_birth,"Gender":sex,"Visa_Expiry_Date":date_of_expiry}
                    print("person_visa_details:",data)
                    filename = visa_number
                    with open('/home/caratred/image/csv/visa/'+ x +'.csv', 'w') as csv_file:
                        writer = csv.writer(csv_file)
                        for key, value in data.items():
                            writer.writerow([key, value])
                    return data
                elif(length==72):
                    act=('\n'.join(tuple(loss)))
                    print("datafh:",act)
                    #print(MRVBCodeChecker(act))
                    type=first[0]
                    print("document type:",type)
                    print("issued state or country:",first[1])
                    issuingcountry=first[2:5]
                    print("issuing country :",issuingcountry)
                    ad=(first[5:]).strip('<')
                    bc=ad.split('<<')
                    surname=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', bc[0])
                    print("sur_name:",surname)
                    if (len(hat)==2):
                        mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', bc[1])
                        givenname=mrx
                        print("given name:",givenname)
                    else:
                        givenname = ''
                        print("given_name:",givenname)
                    print("name of the person:",first[5:])
                    visa_number=second[0:9]
                    print("visa_number:",visa_number)
                    nationality=second[10:13]
                    print("nationality:",nationality)
                    birthdate=second[13:19]
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
                    data={"Visa_Type":type,"Issued_country":issuingcountry,"FamilyName":surname,"Given_Name":givenname,"Visa_Number":visa_number,"Nationality":nationality,"Date_of_Birth":date_of_birth,"Gender":sex,"Visa_Expiry_Date":date_of_expiry}
                    print("person_visa_details:",data)
                    filename = visa_number
                    with open('/home/caratred/image/csv/visa/'+ x +'.csv', 'w') as csv_file:
                        writer = csv.writer(csv_file)
                        for key, value in data.items():
                            writer.writerow([key, value])
                    return data
        detect_text()
