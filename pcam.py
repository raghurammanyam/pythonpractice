"""import cv2
import time
camera = cv2.VideoCapture(0)
image = camera.read()
time.sleep(5)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
print("ksdfnkdsj:",image)
cv2.imshow(image,gray)

cv2.imwrite('/home/opencv.png', image)
del(camera)"""
import cv2
import base64

cap = cv2.VideoCapture(0)
retval, image = cap.read()
retval, buffer = cv2.imencode('.jpg', image)
cv2.imshow('image',image)
cv2.waitKey(100)
jpg_as_text = base64.b64encode(buffer)
print(jpg_as_text)
cap.release()

