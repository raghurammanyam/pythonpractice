
import requests
import io
import os
import json



def detect_text():

    #auto=autorotate(image_file)

    countries_names=[]
    country_codes=[]
    official_names=[]
    #image = Image.open(image_file)
    #greyscale_image = image.convert('L')
    #greyscale_image.save('/home/caratred/image/greyscale_image.jpg')
    #img = cv2.GaussianBlur(image_file, (15,15), 0)
    #img.save('/home/caratred/image/greyscale_image.jpg')
# with open(image_file, 'rb') as image:
    #     base64_image = base64.b64encode(image.read()).decode()
    #print(base64_image)
    url = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAOztXTencncNtoRENa1E3I0jdgTR7IfL0'
    header = {'Content-Type': 'application/json'}
    body =   {"requests": [
    {
    "features": [
        {
        "type": "WEB_DETECTION"
        }
    ],
    "image": {
        "source": {
        "imageUri": "http://i3.kym-cdn.com/photos/images/facebook/000/242/592/1c8.jpg"
        }
    }
    }
    ]
    }

#print("sjdfbgjdfbsgkvdfk",respone_face)
    response = requests.post(url, headers=header, json=body)
    print(response.__dict__)
    text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
    print("text:",text)
detect_text()