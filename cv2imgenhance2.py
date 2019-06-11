import cv2
import numpy as np
from PIL import Image
import pytesseract
import base64
import json
import requests
import re
image = cv2.imread("/home/caratred/Downloads/test/aadharcrop/2019-05-07 16:01:25.836483.jpg")
small = cv2.resize(image, (255,0), fx=1.5, fy=1.5)

img = small

kernel_sharpen_3 = np.array([[-1,-1,-1,-1,-1],
                             [-1,2,2,2,-1],
                             [-1,2,8,2,-1],
                             [-1,2,2,2,-1],
                             [-1,-1,-1,-1,-1]]) / 10.0
#kernel=np.ones((5,5),np.uint8)
#kernel_3x3=np.ones((7,7),np.float32)/49
output_3 = cv2.filter2D(img, -1, kernel_sharpen_3)
output_3=cv2.bilateralFilter(output_3,9,9,5)


#output_3=cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
#output_3=cv2.fastNlMeansDenoisingColored(output_3,None,9,9,10,17)
#output_3=cv2.GaussianBlur(output_3,(7,7),0)
cv2.imwrite('/home/caratred/enhancement.jpeg', output_3)
text = pytesseract.image_to_string(Image.open('/home/caratred/enhancement.jpeg'),lang='guj+eng+tel+tam+ori+mal+hin+ben+kan+pan+sat+mni',config='--psm 12')# --oem 3 -c tessedit_char_whitelist= ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-/.')
# text = text.encode('ascii')
text=re.sub('[^a-zA-Z0-9-/ ]','', text)
#
# print(".....text....:",text)
# osd =pytesseract.image_to_osd(Image.open('/home/caratred/6388aadhardoc.jpeg'))
#
with open('/home/caratred/Downloads/test/aadharcrop/2019-05-07 16:01:25.836483.jpg', 'rb') as image:
     base64_image = base64.b64encode(image.read()).decode()
url = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAOztXTencncNtoRENa1E3I0jdgTR7IfL0'
header = {'Content-Type': 'application/json'}
body = {
    'requests': [{
        'image': {
            'content': base64_image,
        },
        'features': [{
            'type': 'DOCUMENT_TEXT_DETECTION',
            'maxResults': 100,
        }],
        "imageContext":{
        "languageHints":["en-t-iO-handwrit"]
        }
    }]
}
response = requests.post(url, headers=header, json=body).json()
text1 = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
block=str(text).split('\n')
text1=re.sub('[^a-zA-Z0-9-/ ]','', text1)
print("tesseract.......",text)
print("                                                    ")
print("vision ......",text1)
