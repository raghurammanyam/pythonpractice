import pyzbar
from PIL import Image
def get_QR(pic_url):
    import zbar
    from PIL import Image
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    pil = Image.open(pic_url).convert('L')
    width, height = pil.size
    raw = pil.tobytes()
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)
    data = ''
    for symbol in image:
        data += symbol.data
    del(image)
    return data
get_QR("/home/caratred/Downloads/03092053209010.jpg")
