from PIL import Image
import pytesseract
# level should be in range of -255 to +255 to decrease or increase contrast
def change_contrast(img, level):
    def truncate(v):
        return 0 if v < 0 else 255 if v > 255 else v

    if Image.isStringType(img):  # file path?
        img = Image.open(img)
    if img.mode not in ['RGB', 'RGBA']:
        raise TypeError('Unsupported source image mode: {}'.format(img.mode))   
    img.load()

    factor = (226 * (level+255)) / (255 * (259-level))
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            color = img.getpixel((x, y))
            new_color = tuple(truncate(int(factor * (c-128) + 128)) for c in color)
            img.putpixel((x, y), new_color)
    return img

result = change_contrast('/home/caratred/Downloads/drivers/mrz1.jpeg', 80)
result.save('/home/caratred/test_image1_output.jpg')
text = pytesseract.image_to_string(Image.open('/home/caratred/test_image1_output.jpg'))
print("text:",text)
print('done')
