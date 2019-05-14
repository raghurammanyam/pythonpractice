from PIL import Image,ImageEnhance,ImageFilter
import pytesseract

def myEqualize(img):

    im=Image.open(img).convert('L')
    contr = ImageEnhance.Contrast(im)
    im = contr.enhance(1.9)
    bright = ImageEnhance.Brightness(im)
    im = bright.enhance(4.1)
    im.save("/home/caratred/bright.jpeg")
    text = pytesseract.image_to_string(Image.open('/home/caratred/bright.jpeg'))
    print("text:",text)
    return im
myEqualize("/home/caratred/Downloads/drivers/mrz1.jpeg")
