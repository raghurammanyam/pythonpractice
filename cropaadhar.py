from PIL import Image
from os.path import expanduser
home=expanduser('~')

def cropaddress(imagepath):
    image = Image.open(imagepath)
    box = (550, 10, 1000, 200)
    cropped_image = image.crop(box)
    cropped_image.save(home+'/'+'cropped_image.jpg')
    path = home+'/'+'cropped_image.jpg'
    return path
cropaddress('/home/caratred/Downloads/drivers/evisa.jpg')
