from PIL import Image, ExifTags


image = Image.open('/home/caratred/Downloads/drivers/paper_visas/AURORA_CHIAPPI_550_0.jpeg')

#If no ExifTags, no rotating needed.
try:
# Grab orientation value.
    image_exif = image._getexif()
    print("image_exif:",image_exif)
    image_orientation = image_exif[274]

# Rotate depending on orientation.
    if image_orientation == 3:
        rotated = image.rotate(180)
    if image_orientation == 6:
        rotated = image.rotate(-90)
    if image_orientation == 8:
        rotated = image.rotate(90)

# Save rotated image.

    rotated.save('/home/caratred/rotated.jpeg')

except:
    pass
