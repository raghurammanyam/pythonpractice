import os
from PIL import Image
import PIL.ImageOps
num = 0
for root, dirs, files in os.walk("/home/caratred/copy/passport/"):
    for filename in files:
        image = Image.open("/home/caratred/copy/passport/"+filename)
        inverted_image = PIL.ImageOps.invert(image)
        num = num+1
        inverted_image.save('/home/caratred/image/inverted/'+ filename)
