from PIL import Image
import pytesseract
im = Image.open("/home/caratred/Downloads/2019-02-14-141732.jpg").convert('L')
text = pytesseract.image_to_string("/home/caratred/Downloads/2019-02-14-141732.jpg")
print(text)
