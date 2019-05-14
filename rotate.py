import os, re, argparse
from PIL import Image,ExifTags

# this will help you bypass the truncated images
# the truncated images will be completed to full size with gray color.
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


picture_re = re.compile(r'.*\.jpg$', re.IGNORECASE)



def autorotate(path):
    print("dfg")
    """ This function autorotates a picture """
    image = Image.open(path)
    print("dsfggggg")
    try:
        print("ksfnk")
        #exif = image._getexif()
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(image._getexif().items())
        print("kbxckb")
        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)
        image.save(path)
        image.close()
    except AttributeError as e:
        print()
        print ("Could not get exif - Bad image!")
        return False

    (width, height) = image.size
    # print "\n===Width x Heigh: %s x %s" % (width, height)
    if not exif:
        if width > height:
            image = image.rotate(90)
            image.save(path, quality=100)
            return True
    else:
        orientation_key = 274 # cf ExifTags
        if orientation_key in exif:
            orientation = exif[orientation_key]
            rotate_values = {
                3: 180,
                6: 270,
                8: 90
            }
            if orientation in rotate_values:
                # Rotate and save the picture
                image = image.rotate(rotate_values[orientation])
                image.save(path, quality=100, exif=str(exif))
                return path
        else:
            if width > height:
                image = image.rotate(90)
                image.save(path, quality=100, exif=str(exif))

                return path

    return False
