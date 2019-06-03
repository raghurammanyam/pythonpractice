import cv2
import numpy as np
import pytesseract
from PIL import Image
image = cv2.imread("/home/caratred/Downloads/squared/aadhaar/2019-05-07 16:01:25.813277.jpg")
small = cv2.resize(image, (255,0), fx=2.5, fy=2.5)

img = small

kernel_sharpen_3 = np.array([[-1,-1,-1,-1,-1],
                             [-1,2,2,2,-1],
                             [-1,2,8,2,-1],
                             [-1,2,2,2,-1],
                             [-1,-1,-1,-1,-1]]) / 12.0

output_3 = cv2.filter2D(img, -1, kernel_sharpen_3)

#output_3 = cv2.bilateralFilter(output_3,20,16,10)

# output_3 =cv2.GaussianBlur(output_3, (5, 5), 1)
#output_3 = cv2.medianBlur(output_3, 1)


output_3 = cv2.bilateralFilter(output_3,0,85,75)
cv2.imwrite('/home/caratred/enhancement.jpeg', output_3)

text = pytesseract.image_to_string(Image.open('/home/caratred/enhancement.jpeg'),lang='hin+mal+tel+tam+sat+ben+kan+ori+pan+guj+mni+eng',config='--psm 12',nice=2)
print("text:",text)