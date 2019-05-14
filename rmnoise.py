import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open('/home/caratred/Downloads/drivers/224.jpg')  # img is the path of the image 
im = im.convert("L")
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Brightness(im)
im = enhancer.enhance(1.5)
#im = im.convert('1')
nx,ny = im.size
im = im.resize((int(nx*1.5), int(ny*1.5)), Image.ANTIALIAS)
im.save('/home/caratred/temp2.jpg',quality=94)
text = pytesseract.image_to_string(Image.open('/home/caratred/temp2.jpg'))
print(text)