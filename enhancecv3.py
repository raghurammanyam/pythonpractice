import cv2
import pytesseract
from PIL import Image,ImageEnhance,ImageFilter
import os
def crop(image):
    img = cv2.imread(image, 1)
    # cv2.imshow("Original image",img)

    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(9,9))

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels

    l2 = clahe.apply(l)  # apply CLAHE to the L-channel

    lab = cv2.merge((l2,a,b))  # merge channels
    img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    # cv2.imshow('Increased contrast', img2)
    cv2.imwrite('/home/caratred/sunset_modified.jpg', img2)
    text = pytesseract.image_to_string(Image.open('/home/caratred/sunset_modified.jpg'))
    print("text:",text)
    return text
for root, dirs, files in os.walk("/home/caratred/Downloads/croppeddriving"):
         # for filename in files:
        #print(root)
        offence=[crop(root+"/"+x) for x in files]
        offence=[y for x in offence for y in x]
        offence = [x for x in offence if x!='']
        print("offence:",offence)

#cv2.waitKey(0)
# cv2.destroyAllWindows()
