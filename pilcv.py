import cv2
from PIL import Image
import pytesseract
import argparse
import os
import numpy as np

image = cv2.imread('/home/caratred/copy/passport/ANA_RITA_PEREIRA_RIBEIRO_102.jpeg')

#--- dilation on the green channel ---
dilated_img = cv2.dilate(image[:,:,1], np.ones((7, 7), np.uint8))
bg_img = cv2.medianBlur(dilated_img, 21)

#--- finding absolute difference to preserve edges ---
diff_img = 255 - cv2.absdiff(image[:,:,1], bg_img)

#--- normalizing between 0 to 255 ---
norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
cv2.imwrite('/home/caratred/norm_img.png', cv2.resize(norm_img, (0, 0), fx = 1.5, fy = 1.5))
