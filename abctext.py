import base64
import requests
import io
import os
import json
import re
from werkzeug.utils import secure_filename
import datetime
from datetime import date
from PIL import Image
from pprint import pprint
from difflib import get_close_matches
import cv2
from os.path import join
import pycountry
import csv
from collections import defaultdict
import dateparser
from rotate import autorotate


def detect_api(text):
    mrz=[x for x in text if len(x)>=22]
    print(mrz)

    first=re.sub('\‘', '', mrz[0])
    print("first:",first)
    #first=first.replace(first[0],'P',1)
    print("...:",first)
    second =mrz[1]
    if(first[0]=='P'):
        second=re.sub('\‘', '', second)
        type=first[0]
        dat=[x for x in text if len(x)<=12]
        Date_of_issue =''
        ab=''
        for x in dat:
            print(x)
            match = re.search(r'(\d{2} \w+ \/\w+ \d{2}|\d{2} \w+ \d{4}|\d{2} \w+ \d{2}|[0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+ \d{2}|\d{2} \w+/\w+ \d{2}|\d{2} \w+ \w+ \d{2}|\d{2}-\w+-\d{4}|\d{2} \w+\/ \w+ \d{4}|\d{2} \d{2}\. \d{4})', x)
            if match:
                ab=match.group(0)
                print("date:",match.group(0))
                parsed_issue=dateparser.parse(ab,settings={'DATE_ORDER': 'DMY'})
                print("-----:",str(parsed_issue.date()))
                present_date=datetime.datetime.now()
                print("..//...//:",present_date)
                present_year=present_date.year
                issue_date = str(parsed_issue.date())
                year=issue_date[0:4]
                if year<=str(present_year):
                    Date_of_issue=str(parsed_issue.date())

        country_code=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', first[2:5])

        name_with_symbols=first[5:45]

        fullname = name_with_symbols.strip('<')
        name_spliting = fullname.split('<<')
        surname = re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>|\(|\)', ' ', name_spliting[0])

        if (len(name_spliting)==2):
            mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>|\(|\)', ' ', name_spliting[1])
            givenname=mrx
            #print("given name:",givenname)
        else:
            givenname = ''

        document_no=second[0:9]
        passport_no=re.sub(r'[^\w]', ' ',document_no)

        nationality=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', second[10:13])

        birthdate=second[13:19]
        birth_joindate = '/'.join([birthdate[:2],birthdate[2:4],birthdate[4:]])
        #print(birth_joindate)
        parsed_birth=dateparser.parse(birth_joindate,settings={'DATE_ORDER': 'YMD'})
        #print(parsed_birth)
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
        sex=second[20]
        expiry_date=second[21:27]
        expiry_joindate ='/'.join([expiry_date[:2],expiry_date[2:4],expiry_date[4:]])
        parsed_expiry=dateparser.parse(expiry_joindate,settings={'DATE_ORDER': 'YMD'})
        if parsed_expiry==None:
            date_of_expiry =' '
        else:
            date_of_expiry = str((parsed_expiry).date())
        if Date_of_issue == date_of_expiry or Date_of_issue == date_of_birth:
            Date_of_issue= ' '
        print(first)
        #text.remove(first)
        #text.remove(second)
        #print("remove:",text)
        if ab=='':
            text=text
        elif ab!='':
            text.remove(ab)
        print("text:",text)
        text=[x for x in text if x.isalpha()]
        print("afterremove:",text)
        place_of_issue=''
        text=[x for x in text if len(x)>=4]
        if len(text)==1:
            place_of_issue=text[0]
        data={"Document_Type":type,"country_code":country_code,"place_of_issue":place_of_issue,"FamilyName":surname,"Given_Name":givenname,"Date_of_Issue":Date_of_issue,"Passport_Document_No":passport_no,"Nationality":nationality,"Date_of_Birth":date_of_birth,"Gender":sex,"Date_of_Expiry":date_of_expiry}
        details={"type":"PASSPORT","data":data}
        print("person_passport_details:",data)
        return details
    elif(first[0]=='V'):
        second=re.sub('\‘', '', second)
        type=first[0]
        issuingcountry=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', first[2:5])
        entry=''
        Date_of_Issue=''
        dat=[ x for x in text if len(x)<=12]

        for x in dat:
            match = re.search(r'(\d{2} \w+ \d{2}|[0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+ \d{2}|\d{2} \w+/\w+ \d{2}|\d{2} \w+ \w+ \d{2}|\d{2}-\w+-\d{4}|\d{2} \w+\/ \w+ \d{4}|\d{2} \d{2}\. \d{4})', x)
            if match:
                ab=match.group(0)
                #print("date:",match.group(0))
                parsed_issue=dateparser.parse(ab,settings={'DATE_ORDER': 'DMY'})
                #print("-----:",str(parsed_issue.date()))
                Date_of_Issue = str(parsed_issue.date())
        type_of_visa = first[1]
        name_with_symbols=(first[5:]).strip('<')
        fullname=name_with_symbols.split('<<')
        surname=re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>', ' ', fullname[0])
        if (len(fullname)==2):
            mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>', ' ', fullname[1])
            givenname=mrx
        else:
            givenname = ''

        visa_number=re.sub(r'[^\w]', ' ',second[0:9])
        entries=['MULTIPLE','SINGLE','DOUBLE']
        entry=' '
        for y in text[::-1]:
            result = ''.join(i for i in y if not i.isdigit())
            matched_entries=get_close_matches(result,entries)

            if len(matched_entries)==1:
                entry=matched_entries[0]

        nationality=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', second[10:13])
        birthdate = second[13:19]

        birth_joindate = '/'.join([birthdate[:2],birthdate[2:4],birthdate[4:]])
        parsed_birth=dateparser.parse(birth_joindate,settings={'DATE_ORDER': 'YMD'})
        #print(parsed_birth)
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
        sex=second[20]
        expiry_date=second[21:27]

        expiry_joindate='/'.join([expiry_date[:2],expiry_date[2:4],expiry_date[4:]])
        parsed_expiry=dateparser.parse(expiry_joindate,settings={'DATE_ORDER': 'YMD'})
        if parsed_expiry==None:
            date_of_expiry =' '
        else:
            date_of_expiry = str((parsed_expiry).date())
        optional_data=second[28:]
        text.remove(first)
        text.remove(second)
        if ab=='':
            text=text
        elif ab!='':
            text.remove(ab)
        text.remove(entry)
        text=[x for x in text if x.isalpha()]
        print("remain:",text)
        place_of_issue=''
        if len(text)==1:
            place_of_issue=text[0]
        data={"Document_Type":type,"visa_Type":type_of_visa,"place_of_issue":place_of_issue,"Date_of_issue":Date_of_Issue,"Issued_country":issuingcountry,"Visa_No_Of_Enteries":entry,"FamilyName":surname,"Given_Name":givenname,"Visa_Number":visa_number,"Nationality":nationality,"Date_of_Birth":date_of_birth,"Gender":sex,"Visa_Expiry_Date":date_of_expiry}
        details = {"type":"VISA","data":data}
        return details
