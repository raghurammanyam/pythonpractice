from PIL import Image


def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    img.point(contrast)
    img.save('/home/caratred/image/first.png')

change_contrast(Image.open('/home/caratred/copy/passport/ANA_RITA_PEREIRA_RIBEIRO_102.jpeg'), 125)
