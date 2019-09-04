import base64
import requests
import io
import os
import json
import re
import datetime
from datetime import date
from os.path import join
from collections import defaultdict, OrderedDict
from autocorrect import spell
from spellchecker import SpellChecker
from nltk.metrics import edit_distance
from urlextract import URLExtract
from pdf2image import convert_from_path


def extract(image_file):
    #  data   _fields = ['EMPLOYEE NAME:', 'EMERGENCY CONTACT PERSON NAME:', 'CONTACT NO.','EMERGENCY CONTACT PERSON NAME', 'PERMANENT ADDRESS:',
    #                    'PERMANENT ADDRESS', 'CONTACT NO:', 'EXPERIENCE IN YEARS:','FATHER HUSBAND NAME:','FATHER HUSBAND NAME','PRESENT ADDRESS:','PRESENT ADDRESS','FATHER/HUSBAND NAME:','FATHER/HUSBAND NAME','EXPERIENCE IN YEARS', 'NATIVE PLACE:', 'QUALIFICATION:', 'EMAIL ID:','AGE/DATE OF BIRTH:','CONTACT NO:']
    pages = convert_from_path('/home/raghu/Downloads/StatementOfAccount_3121503030_Aug19_183628.pdf', 500)
    for page in pages:
        page.save('/home/raghu/out1234.jpeg', 'JPEG')
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
            "imageContext": {
                "languageHints": ["en-t-iO-handwrit"]
            }
        }]
    }
    response = requests.post(url, headers=header, json=body).json()
    text = response['responses'][0]['textAnnotations'][0]['description'] if len(
        response['responses'][0]) > 0 else ''
   # print(text)
    text_list = str(text).split('\n')
    text_list = [x for x in text_list if len(x) > 2]
   # email_text = ','.join(re.sub(' ','',x) for x in text_list)
    email_text = re.sub(' ', '', text)
    print(email_text)
    # doc=re.compile('(\+\d{2}\d{5}\-\d{5}|\+\d{2}\-\d{3}\-\d{3}-\d{4}|\+\d{2}\-\d{2}\-\d{4}-\d{4}|\+\d{2} \d{5} \d{5}|\+\d{2} \d{4} \d{3} \d{3}|\d{3} \d{4} \d{4}|\+\d{2}\-\d{10}|\+\d{2} \d{10}|\d{10}|\d{5} \d{5}|\+\d{2} \d{2} \d{4} \d{4}|\+d{2} [0-9]{3} \d{3}\-\d{4}|\+\d{2} \d{3} \d{3} \d{4}|\d{3}\-\d{8}|\+\d{2}\-\d+\-\d+|\d{3}\-\d{4} \d{4}|\d{4} \d{3} \d{3}|\+\d{2} \d{2} \d{3} \d{5}|\+\d{2}\-\d{3}\-\d{3}\-\d{4}|\+[0-9]{2} [0-9]{4} [0-9]{6})')
    # mobile_no = doc.findall(text)
    # if len(mobile_no)>=1:
    #     mobileno = mobile_no[0]
    #     print(mobileno)
    # dob_in=re.compile('[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}|[0-9]1,2}\-[0-9]{1,2}\-[0-9]{4}|[0-9]{1,2}\/[0-9]{1,2}\/[0-9]+')
    # date=dob_in.findall(text)
    # if len(date)>=1:
    #     date_of_birth = date[0]
    #     print(date_of_birth)
    empname = ''
    fathername = ''
    native = ''
    study = ''
    email = ''
    experience = ''
    mobile_no = ''
    permanent_address = ''
    present_address = ''
    emp_id = ''
    emergency_name = ''
    extractor = URLExtract()
    urls = extractor.find_urls(email_text)
    urls = [x for x in urls if '@' in x]
    print(urls)
    search = re.compile(
        '([a-zA-Z]+\@[a-zA-Z]+\.[a-zA-Z]+|[a-zA-Z]+\@[a-zA-Z]+\.[a-zA-Z]+\.in$|[a-zA-z]+.[a-zA-Z0-9]+\@[a-zA-Z]+\.[a-zA-Z]+|[a-zA-z]+.[a-zA-Z0-9]+\@[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+)')
    match = search.findall(email_text)
    print(match)
    if len(urls) > 0:
        print(urls[0], "emailid")
    for y in text_list:
        if re.search('EMERGENCY CONTACT PERSON NAME:|EMERGENCY CONTACT PERSON NAME', y):
            emerg_id = text_list.index(y)
        if re.search('PERMANENT ADDRESS:|PERMANENT ADDRESS', y):
            expe_id = text_list.index(y)

    for x in text_list:
        if re.search('EMPLOYEE ID|EMPLOYEED|EMPLOYEE DE', x):
            id_emp = text_list.index(x)
            empid = text_list[id_emp+1]
            if 'EMPLOYEE NAME' not in empid and 'BIO-DATA' not in empid and 'BIODATA' not in empid:
                emp_id = re.sub('[|]|-|#|$| ', '', empid)
        if re.search('EMPLOYEE NAME:|EMPLOYEE NAME', x):
            ind = text_list.index(x)
            emp_name = text_list[ind+1]
            if 'FATHER/HUSBAND NAME' not in emp_name and 'FATHER HUSBAND NAME' not in emp_name:
                empname = emp_name
            # print("empname:", text_list[ind+1])
        if re.search('(FATHER/HUSBAND NAME:|FATHER/HUSBAND NAME|FATHER HUSBAND NAME)', x):
            ind1 = text_list.index(x)
            father = text_list[ind1+1]
            if 'AGE DATE OF BIRTH' not in father and 'AGE/DATE OF BIRTH' not in father:
                fathername = father
                # print("father:", fathername)

        if re.search('(NATIVE PLACE:|NATIVE PLACE)', x):
            ind2 = text_list.index(x)
            native_place = text_list[ind2+1]
            if 'QUALIFICATION' not in native_place:
                native = native_place
            # print("native:", native)

        if re.search('(QUALIFICATION|QUALIFICATION:)', x):
            qual = text_list.index(x)
            study_qual = text_list[qual+1]
            if 'EXPERIENCE IN YEARS' not in study_qual and 'EXPERIENCE' not in study_qual:
                study = study_qual
            # print("study:", study)

        if re.search('(EMAIL ID:|EMAIL ID)', x):
            mail = text_list.index(x)
            email_id = text_list[mail+1]
            if 'PRESENT ADDRESS' not in email_id:
                email = email_id

            # print("mail:", email)

        if re.search('(EXPERIENCE IN YEARS:|EXPERIENCE IN YEARS)', x):
            expe = text_list.index(x)
            experience_work = text_list[expe+1]
            if 'CONTACT NO' not in experience_work:
                experience = experience_work
                # print("experience:", experience)

        if re.search('(CONTACT NO:|CONTACT NO)', x):
            no = text_list.index(x)
            phn_no = text_list[no+1]
            if 'EMAIL ID' not in mobile_no and 'EMAIL' not in mobile_no:
                mobile_no = re.sub('[^0-9-/ ]', '', phn_no)
            # print("mobile_no:", mobile_no)
        if re.search('EMERGENCY CONTACT PERSON NAME:|EMERGENCY CONTACT PERSON NAME', x):
            emerg = text_list.index(x)
            emergency_noun = text_list[emerg+1]
            if 'CELL NO' not in emergency_noun:
                emergency_name = emergency_noun
        if re.search('PERMANENT ADDRESS:|PERMANENT ADDRESS', x):
            expe = text_list.index(x)
            permanent_address = text_list[expe+1:emerg_id]
            permanent_address = ' '.join(x for x in permanent_address)
        if re.search('PRESENT ADDRESS:|PRESENT ADDRESS', x):
            add = text_list.index(x)
            present_address = text_list[add+1:expe_id]
            present_address = ' '.join(x for x in present_address)

    details = {"employee_id": emp_id, "empname": empname, "fathername": fathername, "native_place": native, "qualification": study, "email_id": email, "experience": experience,
               "contact_no": mobile_no, "permanent_address": permanent_address, "emergency_name": emergency_name, "present_address": present_address}
    print(details)


# extract('/home/raghu/Downloads/newform/IMG_20190820_182837.jpg')
for root, dirs, files in os.walk("/home/raghu/Downloads/newform2"):
    for filename in files:
        abc = extract(root+"/"+filename)

# spell = SpellChecker()
# class SpellingReplacer(object):
#     def __init__(self, dict_name = 'en_GB', max_dist = 2):
#         self.spell_dict = enchant.Dict(dict_name)
#         self.max_dist = 2

#     def replace(self, word):
#         if self.spell_dict.check(word):
#             return word
#         suggestions = self.spell_dict.suggest(word)

#         if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
#             return suggestions[0]
#         else:
#             return word

# def spell_check(word_list):
#     checked_list = []
#     for item in word_list:
#         replacer = SpellingReplacer()
#         r = replacer.replace(item)
#         checked_list.append(r)
#     return checked_list
# word_list=['AGUDATA OF BIRTH']
# print(spell_check(word_list))

#    # block=str(text).split('\n')
#     misspelled = spell.unknown(['8th clan','Blamhanawadi','Begumpets','DATA OF BIRTH'])
#     for x in misspelled:
#         print(spell.correction(x))

#     # Get a list of `likely` options
#         print(spell.candidates(x))


#     print(spell("AGUDATA OF BIRTH"))
