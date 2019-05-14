from PIL import Image
from PIL import ExifTags

exifData = {}
img = Image.open('/home/hp/ocr/america.jpg')
exifDataRaw = img._getexif()
for tag, value in exifDataRaw.items():
    decodedTag = ExifTags.TAGS.get(tag, tag)
    exifData[decodedTag] = value
print(exifData)
