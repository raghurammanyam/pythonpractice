import base64
import requests
import io
import os
import json
from PIL import Image, ImageDraw
import re
import datetime
from datetime import date
from mrz.base.countries_ops import is_code
from mrz.checker.td3 import TD3CodeChecker
from mrz.checker.mrva import MRVACodeChecker
from mrz.checker.mrvb import MRVBCodeChecker
from difflib import get_close_matches

import dateparser



def detect_text(image_file):
    loss=[]
    exact_length=[]
    two_lines_mrz=[]
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
    print("text:",text)
    full_text=str(text).split('\n')
    reverse_text=full_text[::-1]
    ca=re.sub(r'\s+', '',str(reverse_text[2]))
    loss.append(ca)
    a=re.sub(r'\s+', '',str(reverse_text[1]))

    loss.append(a)
    print("reverse_text:",reverse_text)
    for x in reverse_text:
        if (len(x)>=25):
            exact_length.append(x)

    line_first = re.sub(r'\s+', '',str(exact_length[1]))
    two_lines_mrz.append(line_first)
    line_second = re.sub(r'\s+', '',str(exact_length[0]))
    two_lines_mrz.append(line_second)
    print(two_lines_mrz,"two_lines_mrz")
    first=two_lines_mrz[0]
    second =two_lines_mrz[1]




    if(first[0]=='P'):

        passport_type=('\n'.join(tuple(loss)))

        type=first[0]
        date_issue=re.findall(r'\s([0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+ \d{2}|\d{2} \w+/\w+ \d{2}|\d{2} \w+ \w+ \d{2}|\d{2}-\w+-\d{4}|\d{2} \w+\/ \w+ \d{4}|\d{2} \d{2}\. \d{4})',text)
        #print("date of birth:",date_issue)
        static  = [' ','.','/','-']
        dates=[]
        for x in date_issue:
                for y in static:
                        if y in (x):
                            if len(x)>7:
                                dates.append(x)

        res = []
        [res.append(x) for x in dates if x not in res]
        parsed_issue=dateparser.parse(res[1],settings={'DATE_ORDER': 'DMY'})
        if parsed_issue==None:
            Date_of_issue=' '
        else:
            issue_join=str((parsed_issue).date())
            Date_of_issue=issue_join

        #Date_of_issue=res[1]
        country_code=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', first[2:5])

        name_with_symbols=first[5:45]

        fullname = name_with_symbols.strip('<')
        name_spliting = fullname.split('<<')
        surname = re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>', ' ', name_spliting[0])

        if (len(name_spliting)==2):
            mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>', ' ', name_spliting[1])
            givenname=mrx
                #print("given name:",givenname)
        else:
            givenname = ''

        document_no=second[0:9]
        passport_no=re.sub(r'[^\w]', ' ',document_no)

        nationality=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', second[10:13])

        birthdate=second[13:19]
        birth_joindate = '/'.join([birthdate[:2],birthdate[2:4],birthdate[4:]])
        parsed_birth=dateparser.parse(birth_joindate,settings={'DATE_ORDER': 'YMD'})
        #print(parsed_birth)
        print(".............................................")
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


        data={"Document_Type":type,"country_code":country_code,"FamilyName":surname,"Given_Name":givenname,"Date_of_Issue":Date_of_issue,"Passport_Document_No":passport_no,"Nationality":nationality,"Date_of_Birth":date_of_birth,"Gender":sex,"Date_of_Expiry":date_of_expiry}
        details={"type":"PASSPORT","data":data}
        print("person_passport_details:",data)
        return details
    elif(first[0]=='V'):
        visa_type=('\n'.join(tuple(loss)))

        type=first[0]
        issuingcountry=re.sub('\ |\?|\.|\!|\/|\;|\:|\<', ' ', first[2:5])
        if (first[1].isalpha()):
            date_issue=re.findall(r'\s([0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+/\w+ \d{4} \w+|\d{2}-\w+-\d{4}|\d{2} \w+\d{4})',text)
            print("date of issue:",date_issue)
            static  = [' ','.','/','-']
            dates=[]
            for x in date_issue:
                    for y in static:
                            if y in (x):
                                if len(x)>7:
                                    dates.append(x)

            issue_date = []
            [issue_date.append(x) for x in dates if x not in issue_date]
            print("date of issue:",issue_date)
            min_year = issue_date[0][6:10]
            if len(issue_date)>1:
                min_year = min(issue_date[0][6:10], issue_date[1][6:10])
            type_of_visa = first[1]
            for x in issue_date:
                if min_year in x:
                    Date=x
                    parsed_issue=dateparser.parse(Date,settings={'DATE_ORDER': 'DMY'})
                    if parsed_issue==None:
                        Date_of_issue=' '
                    else:
                        issue_join=str((parsed_issue).date())
                        Date_of_issue=issue_join
                    #print("great value:",x)
        elif (first[1]=='<'):
            date_issue=re.findall(r'\s([0-9][0-9] [a-zA-Z]+ \d{4}|\d{2}/\d{2}/\d{4}|\d{2}.\d{2}.\d{4}|\d{2} \w+/\w+ \d{4}|\d{2} \d{2} \d{4}|\d{2}-d{2}-d{4}|\d{2} \w+ /\w+ \d{2}|\d{2} \w+/\w+ \d{4} \w+|\d{2}-\w+-\d{4})',text)
            static  = [' ','.','/','-']
            dates=[]
            for x in date_issue:
                    for y in static:
                            if y in (x):
                                if len(x)>7:
                                    dates.append(x)

            issue_date = []
            [issue_date.append(x) for x in dates if x not in issue_date]
            type_of_visa = ' '
            if (len(issue_date)==2):

                Date = issue_date[1]
                parsed_issue=dateparser.parse(Date,settings={'DATE_ORDER': 'DMY'})
                if parsed_issue==None:
                    Date_of_issue=' '
                else:
                    issue_join=str((parsed_issue).date())
                    Date_of_issue=issue_join

            else:
                Date = issue_date[0]
                parsed_issue=dateparser.parse(Date,settings={'DATE_ORDER': 'DMY'})
                if parsed_issue==None:
                    Date_of_issue=' '
                else:
                    issue_join=str((parsed_issue).date())
                    Date_of_issue=issue_join

        entries=['MULTIPLE','SINGLE','DOUBLE']
        entry=' '
        for y in full_text[::-1]:
            result = ''.join(i for i in y if not i.isdigit())
            matched_entries=get_close_matches(result,entries)

            if len(matched_entries)==1:
                entry=matched_entries[0]
                #print("no of entries:",matched_entries[0])
        name_with_symbols=(first[5:]).strip('<')
        fullname=name_with_symbols.split('<<')
        surname=re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>', ' ', fullname[0])
        if (len(fullname)==2):
            mrx=re.sub('\ |\?|\.|\!|\/|\;|\:|\<|\>', ' ', fullname[1])
            givenname=mrx

        else:
            givenname = ''

        visa_number=re.sub(r'[^\w]', ' ',second[0:9])

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
        if Date_of_issue == date_of_expiry or Date_of_issue == date_of_birth:
            Date_of_issue= ' '
        optional_data=second[28:]
        data={"Document_Type":type,"visa_Type":type_of_visa,"Issued_country":issuingcountry,"Visa_No_Of_Enteries":entry,"FamilyName":surname,"Visa_Issue_Date":Date_of_issue,"Given_Name":givenname,"Visa_Number":visa_number,"Nationality":nationality,"Date_of_Birth":date_of_birth,"Gender":sex,"Visa_Expiry_Date":date_of_expiry}
        details = {"type":"VISA","data":data}
        print("person_visa_details:",data)
    return details
detect_text('/home/caratred/Downloads/drivers/IMG-20190424-WA0003.jpg')
