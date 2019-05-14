import cv2
import numpy as np
from PIL import Image, ImageEnhance,ImageFilter,ImageStat
import math
import pytesseract

# Open a typical 24 bit color image. For this kind of image there are
# 8 bits (0 to 255) per color channel
filename='/home/caratred/Downloads/drivers/243.jpg'
img = cv2.imread(filename)  # mandrill reference image from USC SIPfiI
def brightness( im_file ):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   print("brightness of  image:",math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)))
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
brightness(filename)
s = 256
#img = cv2.resize(img, (s,s), 0, 0, cv2.INTER_AREA)

def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


font = cv2.FONT_HERSHEY_SIMPLEX
fcolor = (0,0,0)

#list = [0, -127, 127,   0,  0, 130] # list of brightness values
#clist = [0,    0,   0, -64, 64, 60] # list of contrast values
blist = [90, 124, 127,   80,  133, 100] # list of brightness values
clist = [120,   70,   52, 44, 57, 70] 
out = np.zeros((s*2, s*3, 3), dtype = np.uint8)

for i, b in enumerate(blist):
    c = clist[i]
    print('b, c:  ', b,', ',c)
    row = s*int(i/3)
    col = s*(i%3)

    #print('row, col:   ', row, ', ', col)

    #out[row:row+s, col:col+s] = apply_brightness_contrast(img, b, c)
    out=apply_brightness_contrast(img, b, c)
    cv2.imwrite('/home/caratred/out'+str(i)+'.jpeg', out)
    text = pytesseract.image_to_string(Image.open('/home/caratred/out'+str(i)+'.jpeg'))
    print("text:",text)
    W = 1000.
    oriimg = cv2.imread('/home/caratred/out'+str(i)+'.jpeg')
    height, width, depth = oriimg.shape
    imgScale = W/width
    newX,newY = oriimg.shape[2]*imgScale, oriimg.shape[2]*imgScale
    newimg = cv2.resize(oriimg,(int(6000),int(6000)))
    cv2.imwrite("/home/caratred/resize"+str(i)+'.jpeg',newimg)
    cv2.imshow('after',out)
    brightness("/home/caratred/resize"+str(i)+'.jpeg')
    #msg = 'b %d' % b
    #cv2.putText(out,msg,(col,row+s-22), font, .7, fcolor,1,cv2.LINE_AA)
    #msg = 'c %d' % c
    #cv2.putText(out,msg,(col,row+s-4), font, .7, fcolor,1,cv2.LINE_AA)

    #cv2.putText(out, 'OpenCV',(260,30), font, 1.0, fcolor,2,cv2.LINE_AA)

    #break
# cv2.imwrite('/home/caratred/out.jpeg', out)
# W = 1000.
# oriimg = cv2.imread('/home/caratred/out.jpeg')
# height, width, depth = oriimg.shape
# imgScale = W/width
# newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
# newimg = cv2.resize(oriimg,(int(1200),int(1200)))
# cv2.imwrite("/home/caratred/resize.jpeg",newimg)
# cv2.imshow('after',out)