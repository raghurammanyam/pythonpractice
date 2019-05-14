import random
import cv2
import sys
import os
from os.path import expanduser
from datetime import date, datetime
date = str(date.today())
home =  expanduser('~')
directory_concatenation = home +'/'+date+'/'

CASCADE="Har_cascade.xml"
FACE_CASCADE=cv2.CascadeClassifier(CASCADE)
rand_int=random.randint(0,10000)

def detect_faces(image_path,number):
    image=cv2.imread(image_path)
    file_path = image_path.strip(directory_concatenation)
    image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.16,minNeighbors=5,minSize=(30,50),flags=0)
    for x,y,w,h in faces:
        sub_img=image[y-20:y+h+95,x-10:x+w+35]


        cv2.imwrite(home +'/'+'xxxx'+str(number)+'face.jpeg',sub_img)


        cv2.rectangle(image,(x,y),(x+w,y+h),(255, 255,0),2)

        break
    path=home +'/'+'xxxx'+str(number)+'face.jpeg'

    return path
detect_faces('/home/caratred/Downloads/drivers/IMG-20190424-WA0002.jpg',1)
