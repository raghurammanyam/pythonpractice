import cv2 
import numpy as np 
from PIL import Image, ImageEnhance,ImageFilter
import pytesseract
  
# Reading the input image 
img = cv2.imread('/home/caratred/Downloads/drivers/mrz1.jpeg', 2) 
  
# Taking a matrix of size 5 as the kernel 
kernel = np.ones((5,5), np.uint8) 
  
# The first parameter is the original image, 
# kernel is the matrix with which image is  
# convolved and third parameter is the number  
# of iterations, which will determine how much  
# you want to erode/dilate a given image.  
img_erosion = cv2.erode(img, kernel, iterations=1) 
img_dilation = cv2.dilate(img, kernel, iterations=1)
(height, width) = img.shape[:3] 
  
    # Specify the size of image along with interploation methods. 
    # cv2.INTER_AREA is used for shrinking, whereas cv2.INTER_CUBIC 
    # is used for zooming. 
res = cv2.resize(img, (int(width * 1.5), int(height * 1.5)), interpolation = cv2.INTER_AREA) 
   
  
cv2.imshow('Input', img) 
cv2.imshow('Erosion', res) 
cv2.imshow('Dilation', img_dilation)
cv2.imwrite("/home/caratred/noise.jpeg",res) 
cv2.imwrite("/home/caratred/dialate.jpeg",res)
cv2.imwrite("/home/caratred/input.jpeg",res)
text = pytesseract.image_to_string(Image.open('/home/caratred/input.jpeg'))
print("text:",text)
text = pytesseract.image_to_string(Image.open('/home/caratred/noise.jpeg'))
print("text:",text)

  
cv2.waitKey(0) 