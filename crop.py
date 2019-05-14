from PIL import Image,ImageEnhance,ImageFilter
import pytesseract
import cv2
import os
import imutils
import numpy as np
from abctext import detect_api

def imagetext():
    images=['/home/caratred/Downloads/drivers/224.jpg','/home/caratred/copy/passport/issue12.jpeg','/home/caratred/Downloads/drivers/place23.jpeg']
    def imgenhance(imgpath):
        img = Image.open(imgpath).convert("L")
        img = img.filter(ImageFilter.SHARPEN())
        enhancer = ImageEnhance.Brightness(img)
        out = enhancer.enhance(1.8)
        nx, ny = out.size
      #  print("imagesize:",nx,ny)
        out = out.resize((int(nx*1.5), int(ny*1.5)), Image.ANTIALIAS)
        print("size:",out.size)
        out.save("/home/caratred/copy/passport/Cleaned1.jpeg",quality=94)
        out.show()
        text = pytesseract.image_to_string(Image.open('/home/caratred/copy/passport/Cleaned1.jpeg'))
        extract=text.split('\n')
        print(extract)
        return extract
    offence=[imgenhance(x) for x in images]
    offence=[y for x in offence for y in x]
    offence = [x for x in offence if x!='']
    print("offence:",offence)
    abc = detect_api(offence)
    print(abc)
    return abc
imagetext()
