import base64
import requests
header = {'Content-Type': 'application/json'}
url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyCJ5L8oL4eus610m7dOVeF8QjfIkAmM7ew'
file_name = '/home/hp/ocr/pas.jpeg'
with open(file_name, 'rb') as image:
    image_content = image.read()
    encoded_content = base64.b64encode(image_content).decode()
    #print(encoded_content)

data = {
  "requests":[
    {
      "image":{
      "content": encoded_content
    },
  "features":[
    {
      "type":"TEXT_DETECTION",
      "maxResults":1
    }
   ]
  }
 ]
}
print("data",data)
r = requests.post(url=url,headers=header,json=data).json()
#print("textuabledata:",r.text)
#x = json.loads(r.text)
#print("kjfbgadkf:",x)
print(r['responses'][0]['textAnnotations'][0]['description'])
