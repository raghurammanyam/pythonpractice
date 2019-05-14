import cv2
import os
import numpy as np
# arr = os.listdir('/home/caratred/Downloads/votecard')
#
# for root, dirs, files in os.walk("/home/caratred/Downloads/votecard"):
#
#     for filename in files:


img = cv2.imread('/home/caratred/6388aadhardoc.jpeg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,5,255,cv2.THRESH_BINARY)
_,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
x,y,w,h = cv2.boundingRect(cnt)
crop = img[y:y+h,x:x+w]
cv2.imwrite('/home/caratred/blacktrim.jpeg',crop)










        # print(root+"/"+filename)
        # img = cv2.imread(root+"/"+filename)
        # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # _,thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
        # _, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cnt = contours[0]
        # x,y,w,h = cv2.boundingRect(cnt)
        # crop = img[y:y+h,x:x+w]
        # cv2.imwrite('/home/caratred/cropedImages/'+filename,crop)
