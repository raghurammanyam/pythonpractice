from PIL import Image

from PIL import ImageEnhance

def adjust_sharpness(input_image, output_image, factor):

    image = Image.open(input_image)

    enhancer_object = ImageEnhance.Sharpness(image)

    out = enhancer_object.enhance(factor)

    out.save(output_image)

if __name__ == '__main__':

    adjust_sharpness('/home/caratred/copy/passport/BARUCH_TRATTNER_672.jpeg',

                     '/home/caratred/image/passports/Canada1.png',

                     9.0)
