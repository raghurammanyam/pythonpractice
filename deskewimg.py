import cv2
import numpy as np


import numpy as np
import math
import cv2
import cv2
import numpy as np

# get the minimum bounding box for the chip image
image = cv2.imread("/home/caratred/Downloads/test/aadharcrop/2019-05-07 16:01:27.233601.jpg", cv2.IMREAD_COLOR)
image = image[50:-1,0:-1]
imgray = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)[...,0]
ret, thresh = cv2.threshold(imgray, 20, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
print(thresh,"tresh")
mask = 25 - thresh
print(mask)
_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

maxArea = 0
best = None
for contour in contours:
  area = cv2.contourArea(contour)
  if area > maxArea :
    maxArea = area
    best = contour

rect = cv2.minAreaRect(best)
box = cv2.boxPoints(rect)
box = np.int0(box)

#crop image inside bounding box
scale = 1  # cropping margin, 1 == no margin
W = rect[1][0]
H = rect[1][1]

Xs = [i[0] for i in box]
Ys = [i[1] for i in box]
x1 = min(Xs)
x2 = max(Xs)
y1 = min(Ys)
y2 = max(Ys)

angle = rect[2]
rotated = False
if angle < -45:
    angle += 90
    rotated = True

center = (int((x1+x2)/2), int((y1+y2)/2))
size = (int(scale*(x2-x1)), int(scale*(y2-y1)))

M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)

cropped = cv2.getRectSubPix(image, size, center)
cropped = cv2.warpAffine(cropped, M, size)

croppedW = W if not rotated else H
croppedH = H if not rotated else W

image = cv2.getRectSubPix(
    cropped, (int(croppedW*scale), int(croppedH*scale)), (size[0]/2, size[1]/2))

# # show result
# while True:
#   #cv2.imshow("result", image)
cv2.imwrite("/home/caratred/abcdeskew.jpeg",image)
