import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

image = cv2.imread("/home/caratred/Downloads/images/drivingcrop/15.JPG")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
kernel = np.ones((1, 1), np.uint8)
gray = cv2.dilate(gray, kernel, iterations=1)
gray = cv2.erode(gray, kernel, iterations=1)
#gray = cv2.medianBlur(gray, 3)
gray = cv2.GaussianBlur(gray, (9, 9), 0)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
gray = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
#gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#gray = cv2.threshold(gray, 0, 250, cv2.THRESH_BINARY_INV)
gray=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31,2)
#gray = cv2.medianBlur(gray, 3)
gray = cv2.resize(gray, None, fx=3.4, fy=3.4, interpolation=cv2.INTER_CUBIC)
filename="/home/caratred/gray.png"
cv2.imwrite(filename, gray)
text = pytesseract.image_to_string(Image.open(filename))
print(text)
