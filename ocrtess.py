import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open("/home/caratred/copy/passport/mrz12.jpeg").convert('RGB') # the second one
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Brightness(im)
im = enhancer.enhance(1.7)

im.save('/home/caratred/temp2.jpg')
text = pytesseract.image_to_string(Image.open('/home/caratred/temp2.jpg'))
print(text)
