import cv2
import numpy as np


QR_orig = cv2.imread('/home/caratred/Downloads/drivers/evisa.jpg', 0)
QR = cv2.imread('/home/caratred/Downloads/drivers/qr.jpg', 0) # read the QR code binary image as grayscale image to make sure only one layer
mask = np.zeros(QR.shape,np.uint8) # mask image the final image without small pieces

# using findContours func to find the none-zero pieces
#_,contours, hierarchy = cv2.findContours(QR,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

# draw the white paper and eliminate the small pieces (less than 1000000 px). This px count is the same as the QR code dectection
best = 0
maxsize = 0
count = 0
for cnt in contours:
    if cv2.contourArea(cnt) > maxsize :
        maxsize = cv2.contourArea(cnt)
        best = count

    count = count + 1

x,y,w,h = cv2.boundingRect(cnt[best])
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        # crop the original QR based on the ROI
        QR_crop = QR_orig[y:y+h,x:x+w]
        # use cropped mask image (roi) to get rid of all small pieces
        QR_final = QR_crop * (roi/255)
cv2.imwrite('/home/raghu/QR_final.jpg',QR_final)
