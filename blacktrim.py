import cv2
import numpy as np

# Read the image
img = cv2.imread('/home/caratred/6388aadhardoc.jpeg')

# Get image shape
h, w, channels = img.shape

# Draw a rectangle on the border to combine the wall to one contour
cv2.rectangle(img,(0,0),(w,h),(0,0,0),2)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply binary threshold
_, threshold = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)

# Search for contours and sort them by size
_, contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
area = sorted(contours, key=cv2.contourArea, reverse=True)

# Draw it out with white color from biggest to second biggest contour
cv2.drawContours(img, ((contours[0]),(contours[1])), -1, (255,255,255), -1)

# Apply binary threshold again to the new image to remove little noises
_, img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)

# Display results
cv2.imshow('img', img)
cv2.imwrite('/home/caratred/cropedImages/aadhar.jpeg',img)
