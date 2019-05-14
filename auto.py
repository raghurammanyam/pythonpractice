from PIL import Image
import imdirect
img = Image.open('/home/caratred/Downloads/drivers/imageedit_2_3347203087.jpg')
print(img)
img_rotated = imdirect.autorotate(img)
