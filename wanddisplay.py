import numpy as np
from PIL import Image
import pytesseract

# Open the input image as numpy array, convert to greyscale and drop alpha
npImage=np.array(Image.open("/home/caratred/Downloads/drivers/mrz1.jpeg").convert("L"))

# Get brightness range - i.e. darkest and lightest pixels
min=np.min(npImage)        # result=144
max=np.max(npImage)        # result=216
print(max,min)
# Make a LUT (Look-Up Table) to translate image values
LUT=np.zeros(256,dtype=np.uint8)
LUT[min:max+1]=np.linspace(start=0,stop=239,num=(max-min)+1,endpoint=True,dtype=np.uint8)

# Apply LUT and save resulting image
Image.fromarray(LUT[npImage]).save('/home/caratred/result.jpeg')
text = pytesseract.image_to_string(Image.open('/home/caratred/result.jpeg'))
print("text:",text)