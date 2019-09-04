import cv2
import numpy as np
import pytesseract
from PIL import Image
def enhance(image):
        print(",.")
        image = cv2.imread(image)
        print("..//")
        small = cv2.resize(image, (200,0), fx=2.5, fy=2.5)

        img = small

        kernel_sharpen_3 = np.array([[-1,-1,-1,-1,-1],
                                [-1,2,8,2,-1],
                                [-1,2,4,2,-1],
                                [-1,4,4,4,-1],
                                [-1,-1,-1,-1,-1]]) / 12.0

        output_3 = cv2.filter2D(img, -1, kernel_sharpen_3)

        #output_3 = cv2.bilateralFilter(output_3,20,16,10)

        # output_3 =cv2.GaussianBlur(output_3, (5, 5), 1)
#        output_3 = cv2.medianBlur(output_3,3)

#        output_3 = cv2.fastNlMeansDenoisingColored(output_3,None,6,6,7,21)
        output_3 = cv2.bilateralFilter(output_3,0,75,75)
        #output_3 =cv2.adaptiveThreshold(output_3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        cv2.imwrite('/home/raghu/enhancement.jpeg', output_3)

        text = pytesseract.image_to_string(Image.open('/home/raghu/enhancement.jpeg'),lang='hin+mal+tel+tam+sat+ben+kan+ori+pan+guj+mni+eng',config='--psm 11')
        print("text:",text)


enhance("/home/raghu/Downloads/squared/aadhaar/abc3.jpg")