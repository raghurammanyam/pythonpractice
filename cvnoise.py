from PIL import Image,ImageEnhance,ImageFilter
import pytesseract
import cv2
from os.path import expanduser
home = expanduser('~')
import numpy as np
#print(home)
img = cv2.imread('/home/caratred/Downloads/drivers/224.jpg', cv2.IMREAD_COLOR)
imgBlur = cv2.GaussianBlur(img, (9, 9), 0)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
imgTH = cv2.morphologyEx(imgBlur, cv2.MORPH_TOPHAT, kernel)
_, imgBin = cv2.threshold(imgTH, 0, 250, cv2.THRESH_OTSU)

imgdil = cv2.dilate(imgBin, kernel)
_, imgBin_Inv = cv2.threshold(imgdil, 0, 250, cv2.THRESH_BINARY_INV)

cv2.imshow('original', image)
cv2.imshow('bin', imgBin)
cv2.imshow('dil', imgdil)
cv2.imshow('inv', imgBin_Inv)

cv2.imwrite(home+'/ocrnoise.jpeg', imgBin_Inv)
cv2.waitKey(0)
text = pytesseract.image_to_string(Image.open(home+'/ocrnoise.jpeg'))
print(".....text....:",text)
