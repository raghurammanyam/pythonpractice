from pyimagesearch import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils


 #load the image and grab the source coordinates (i.e. the list of
# of (x, y) points)
# NOTE: using the 'eval' function is bad form, but for this example
# let's just roll with it -- in future posts I'll show you how to
# automatically determine the coordinates without pre-supplying them
image = cv2.imread("/home/caratred/aadhar.jpeg")
pts = np.array(eval("/home/caratred/aadhar.jpeg"), dtype = "float32")
 
# apply the four point tranform to obtain a "birds eye view" of
# the image
warped = four_point_transform(image, pts)
 
# show the original and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)