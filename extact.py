import cv2
import numpy as np
from PIL import Image
import pytesseract
# Read the image and create a blank mask
img = cv2.imread('/home/caratred/Downloads/images/drivingcrop/85.JPG')
h,w = img.shape[:2]
mask = np.zeros((h,w), np.uint8)

# Transform to gray colorspace and invert Otsu threshold the image
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray,255,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# ***OPTIONAL FOR THIS IMAGE

### Perform opening (erosion followed by dilation)
#kernel = np.ones((2,2),np.uint8)
#opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# ***

# Search for contours, select the biggest and draw it on the mask
_, contours, hierarchy = cv2.findContours(thresh, # if you use opening then change "thresh" to "opening"
                                          cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnt = max(contours, key=cv2.contourArea)
cv2.drawContours(mask, [cnt], 0, 255, -1)

# Perform a bitwise operation
res = cv2.bitwise_and(img, img, mask=mask)

########### The result is a ROI with some noise
########### Clearing the noise

# Create a new mask
mask = np.zeros((h,w), np.uint8)

# Transform the resulting image to gray colorspace and Otsu threshold the image
gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Search for contours and select the biggest one again
_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnt = max(contours, key=cv2.contourArea)
#print("lsnnkgfnksdr:",cnt)
#cv2.imwrite("/home/caratred/noisy.jpeg",cnt)
# Draw it on the new mask and perform a bitwise operation again
cv2.drawContours(mask, [cnt], 0, 0, 255)
res = cv2.bitwise_and(img, img, mask=mask)

# If you will use pytesseract it is wise to make an aditional white border
# so that the letters arent on the borders
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(res,(x,y),(x+w,y+h),(255,0,255),1)

# Crop the result
final_image = res[y:y+h+1, x:x+w+1]

# Display the result
cv2.imshow('img', final_image)
cv2.imwrite("/home/caratred/ss.jpeg",final_image)
text = pytesseract.image_to_string(Image.open('/home/caratred/ss.jpeg'))
print(".....text....:",text)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
