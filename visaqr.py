from PIL import Image
from pyzbar.pyzbar import decode
import re
import xmltodict

def qr_scan(img_path):
    data = decode(Image.open(img_path))
    #print("ksbsdjfbgjdf:",data)
    qr_extracted_data=(data[0][0]).decode("utf-8")
    d=(xmltodict.parse(qr_extracted_data,process_namespaces=True))
    original=d['applicant']
    person_data=dict(original)
    #print("data_retrived:",qr_extracted_data)
    print("......,:",d,person_data)
    Visa_Number=person_data['visaNumber']
    Given_Name = person_data['applname']
    passportNumber=person_data['passportNumber']
    details = {'Visa_Number':Visa_Number,"Given_Name":Given_Name,"passportNumber":passportNumber}
    print(details)
    return details
    person_address=[]
    #abc=(xmltodict.parse(qr_extracted_data,process_namespaces=True))
    #manual=abc['QPDB']
    #print("..........//:",dict(manual))
    if '"UTF-8"?>\n' in qr_extracted_data:
        d=(xmltodict.parse(qr_extracted_data,process_namespaces=True))
        print(".....:",d)
        original=d['PrintLetterBarcodeData']
        person_data=dict(original)
        #print(person_data.values())
        print("////////:",person_data)
        for key,value in person_data.items():
            person_address.append(value)
        print("person_address:",person_address)
    elif '"UTF-8"?> <' in qr_extracted_data:

        rply = qr_extracted_data.replace('UTF-8?">','UTF-8"?>\n')

        d=(xmltodict.parse(rply,process_namespaces=True))
        print(".....:",d)
        original=d['PrintLetterBarcodeData']
        person_data=dict(original)
        print("data_json:",person_data)
        for key,value in person_data.items():
            person_address.append(value)
        print("person_address:",person_address)
    elif '"utf-8?"><' in qr_extracted_data:
        rply = qr_extracted_data.replace('utf-8?">','utf-8"?>\n')
        d=(xmltodict.parse(rply,process_namespaces=True))
        print(".....:",d)
        original=d['PrintLetterBarcodeData']
        person_data=dict(original)
        print("////////:",person_data)
        for key,value in person_data.items():
            if value!='':
                person_address.append(value)
        print("person_address:",person_address)
qr_scan("/home/caratred/Downloads/drivers/qr.jpg")

#print(str(data))
