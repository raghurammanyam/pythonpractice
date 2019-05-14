from __future__ import print_function
import numpy as np
import argparse
import cv2
import cv2
import numpy as np
from matplotlib import pyplot as plt
from cycler import cycler
from PIL import Image, ImageEnhance
import pytesseract

# Loads the image then enhances it
#image = Image.open('/home/caratred/Downloads/drivers/243.jpg')
image = cv2.imread('/home/caratred/Downloads/drivers/mrz2.jpeg',0)
#contrast = ImageEnhance.Brightness(image)
#img=contrast.enhance(3.9)
#img = np.asarray(img)
#print(img)
# equ = cv2.equalizeHist(image)
# res = np.hstack((image,equ))
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
cl1 = clahe.apply(image)


"""
r, g, b = cv2.split(img)
contrast=cv2.merge([b, g, r])
# Reads the enhanced image and converts it to grayscale, creates new file
gray_image = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY) #there is a problem here


# Adaptive Gaussian Thresholding
th1 = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY,11,2)
# Otsu's thresholding
ret2,th2 = cv2.threshold(th1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(th2,(5,5),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)"""

# writes enhanced and thresholded img
cv2.imwrite('/home/caratred/enhancedGrayscaleThresholdLineCapture.jpeg', cl1)
text = pytesseract.image_to_string(Image.open('/home/caratred/enhancedGrayscaleThresholdLineCapture.jpeg'))
print("text:",text)
