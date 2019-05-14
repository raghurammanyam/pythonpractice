from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import os
import random
import pytesseract
from vision import detect_text
from PIL import Image, ImageEnhance, ImageFilter
import base64

rand_int=random.randint(0,10000)


rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
def image_search(imagepath):

	# load the image, resize it, and convert it to grayscale
    print("image_path:",imagepath)
    image = cv2.imread(imagepath)
    image = imutils.resize(image, height=600)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# smooth the image using a 3x3 Gaussian, then apply the blackhat
	# morphological operator to find dark regions on a light background
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
    	# compute the Scharr gradient of the blackhat image and scale the
	# result into the range [0, 255]
    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=4)
    p = int(image.shape[1] * 0.05)
    thresh[:, 0:p] = 0
    thresh[:, image.shape[1] - p:] = 0
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        crWidth = w / float(gray.shape[1])
        if ar > 5 and crWidth > 0.75:
            pX = int((x + w) * 0.03)
            pY = int((y + h) * 0.11)
            (x, y) = (x - pX, y - pY)
            (w, h) = (w + (pX * 2), h + (pY * 2))
			# extract the ROI from the image and draw a bounding box
			# surrounding the MRZ
            roi = image[y:y + h, x:x + w].copy()
            os.chdir("Extracted")
            bc=cv2.imwrite(str(rand_int)+".jpg",roi)
            os.chdir("../")
            path='/home/caratred/image/Extracted/'+str(rand_int)+'.jpg'
            print("details:",bc,path)
            #print("image:",(image[y:y + h, x:x + w]+".jpg"))
            #base64_image = base64.b64encode((image[y:y + h, x:x + w]).read()).decode()
            #print("buffer data:",base64_image)
            abc=detect_text(path)
            #text = pytesseract.image_to_string(Image.open(path),config='-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz -psm 6', lang='eng')
            print(abc)



            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break
    cv2.imshow("Image", image)
    cv2.imshow("ROI", roi)
    #print(cv2.imwrite(str(rand_int)+".jpg",roi))
    cv2.waitKey(0)
image_search("/home/caratred/image/passports/Canada.png")
