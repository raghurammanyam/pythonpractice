from pyzbar.pyzbar import decode
import cv2
import numpy as np
from pyzbar.pyzbar import ZBarSymbol
from PIL import Image
def barcodeReader(image):
    image = cv2.imread(image)
    barcodes = decode(image)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        barcodeData = barcode.data.decode('utf-8')
        barcodeType = barcode.type
        text = "{} ( {} )".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)

        print("Information : \n Found Type : {} Barcode : {}".format(barcodeType, barcodeData))

    cv2.imshow("Image", image)
    cv2.waitKey(0)
        
barcodeReader('/home/raghu/thaiid_parser/static/capture.jpg')




# image= cv2.imread(image)

#     height, width = image.shape[:2]
#     grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     #data=decode((grey.tobytes(), width, height))
#     data=decode((image[:, :, 0].astype('uint8').tobytes(), width, height))
data1=decode(Image.open('/home/raghu/Downloads/IMG_20191114_121246.jpg'), symbols=[ZBarSymbol.CODE128])
print(data1)