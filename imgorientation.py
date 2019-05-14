# from img_rotate import fix_orientation
# img= '/home/caratred/Downloads/VALERIE BEATRICE_MOGLIA_347.jpeg'
# fix_orientation(img, save_over=True)
from PIL import ExifTags
from PIL import Image

# img = Image.open('/home/caratred/112295153.jpg')
# print(img._getexif().items())
# exif=dict((ExifTags.TAGS[k], v) for k, v in img._getexif().items() if k in ExifTags.TAGS)
# if not exif['Orientation']:
#     img=img.rotate(90, expand=True)
# img.thumbnail((1000,1000), Image.ANTIALIAS)
# img.save('/home/caratred/rotatedimage.jpeg', "JPEG")
# img.show()
# from PIL import Image, ExifTags
#
# # Open file with Pillow
# image = Image.open('/home/caratred/112295153.jpg')
#
# #If no ExifTags, no rotating needed.
# try:
# # Grab orientation value.
#     image_exif = image._getexif()
#     print(image_exif)
#     image_orientation = image_exif[274]
#
# # Rotate depending on orientation.
#     if image_orientation == 3:
#         rotated = image.rotate(180)
#     if image_orientation == 6:
#         rotated = image.rotate(-90)
#     if image_orientation == 8:
#         rotated = image.rotate(90)
#
# # Save rotated image.
#     rotated.save('/home/caratred/rotatedimage.jpeg')
# except:
#     print("jjjjjjjjjjj")
#     pass
from PIL import Image
import piexif

def rotate_jpeg():
    print("llk")
    img = Image.open('/home/caratred/2018-12-21X51234567_GAIMU.png')
    print(img.info)
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])
        print(exif_dict)

        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
            exif_bytes = piexif.dump(exif_dict)

            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

            img.save('home/caratred/rotatedimage.jpeg', exif=exif_bytes)
rotate_jpeg()
