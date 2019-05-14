import cv2
import numpy as np
import sys
import time

def x_scan(img_path):
    inputImage = cv2.imread(img_path)
    def display(im, bbox):
        n = len(bbox)
        for j in range(n):
            cv2.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255,0,0), 3)

        # Display results
        cv2.imshow("Results", im)
    qrDecoder = cv2.QRCodeDetector()

    # Detect and decode the qrcode
    data,bbox,rectifiedImage = qrDecoder.detectAndDecode(inputImage)
    if len(data)>0:
        print("Decoded Data : {}".format(data))
        display(inputImage, bbox)
        rectifiedImage = np.uint8(rectifiedImage);
        cv2.imshow("Rectified QRCode", rectifiedImage);
    else:
        print("QR Code not detected")
        cv2.imshow("Results", inputImage)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
x_scan("/home/caratred/Downloads/03092053209010.jpg")
