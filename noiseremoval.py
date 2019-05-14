import numpy as np
import cv2
from matplotlib import pyplot as plt
import cv2
import numpy as np


image = cv2.imread('/home/caratred/Downloads/342i.jpeg')
kernel = np.ones((3,3),np.float32)/10
processed_image = cv2.filter2D(image,-1,kernel)

cv2.imshow('before filter processing:',image)
cv2.imshow('Mean Filter Processing', processed_image)
cv2.imwrite('/home/caratred/processed_image.jpeg', processed_image)
