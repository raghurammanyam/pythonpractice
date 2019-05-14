import cv2

camera = cv2.VideoCapture(0)
for i in range(10):
    return_value, image = camera.read()
    cv2.imwrite('/home/caratred/web.jpeg', image)
del(camera)
