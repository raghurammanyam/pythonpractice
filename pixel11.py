from PIL import Image
from PIL import ImageFilter,ImageEnhance
import pytesseract

file = '/home/caratred/Downloads/drivers/attachments/IMG_20190213_112301460_1.jpg'
img = Image.open(file).convert('L')
img = img.filter(ImageFilter.SHARPEN())

enhancer = ImageEnhance.Brightness(img)
out = enhancer.enhance(1.8)
nx, ny = out.size
out = out.resize((int(nx*1.8), int(ny*1.8)), Image.ANTIALIAS)
out.save('/home/caratred/img.jpeg')
text = pytesseract.image_to_string(Image.open('/home/caratred/img.jpeg'))
print("text:",text)
