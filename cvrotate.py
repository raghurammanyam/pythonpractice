import cv2
import imutils
import numpy as np

PIC_PATH = "/home/caratred/Downloads/drivers/paper_visas/AURORA_CHIAPPI_550_0.jpeg"    

image = cv2.imread(PIC_PATH)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

edged = cv2.Canny(gray, 100, 220)

kernel = np.ones((5,5),np.uint8)
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

cv2.drawContours(image, cnts, -1, (0, 255, 0), 4)

cv2.imshow("Output", image)
cv2.waitKey(0)
