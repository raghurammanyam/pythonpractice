from PIL import Image,ImageEnhance,ImageFilter
import pytesseract
import cv2
import os
import imutils
import numpy as np
from abctext import detect_api

#def imagetext():
    #images=['/home/caratred/Downloads/drivers/224.jpg','/home/caratred/copy/passport/issue12.jpeg','/home/caratred/Downloads/drivers/place23.jpeg']
def imgenhance(imgpath):
    img = Image.open(imgpath).convert("L")#.histogram()

    img = img.filter(ImageFilter.SHARPEN())
    enhancer = ImageEnhance.Contrast(img)
    out = enhancer.enhance(0.3)
    enhancer=ImageEnhance.Brightness(out)
    out = enhancer.enhance(2.0)
    nx, ny = out.size
  #  print("imagesize:",nx,ny)
    out = out.resize((int(nx*1.5), int(ny*1.5)), Image.ANTIALIAS)
    #print("size:",out.size)
    out.save("/home/caratred/copy/passport/Cleaned1.jpeg",quality=94)
    #out.show()
    text = pytesseract.image_to_string(Image.open("/home/caratred/copy/passport/Cleaned1.jpeg"))
    print(text)
    extract=text.split('\n')
    print(extract)
    return extract
imgenhance('/home/caratred/Downloads/images/drivingcrop/15.JPG')
    # offence=[imgenhance(x) for x in images]
    # offence=[y for x in offence for y in x]
    # offence = [x for x in offence if x!='']
    # print("offence:",offence)
    #abc = detect_api(offence)
    #print(abc)
    #return offence
# for root, dirs, files in os.walk("/home/caratred/Downloads/croppeddriving"):
#          # for filename in files:
#         #print(root)
#         offence=[imgenhance(root+"/"+x) for x in files]
#         offence=[y for x in offence for y in x]
#         offence = [x for x in offence if x!='']
#         print("offence:",offence)
