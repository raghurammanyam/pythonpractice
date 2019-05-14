import numpy as np
import cv2
import os
for root, dirs, files in os.walk("/home/caratred/Downloads/test/aadhaar"):
         for filename in files:
                print(filename)
                img = cv2.imread(root+"/"+filename) # Read in the image and convert to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
                coords = cv2.findNonZero(gray) # Find all non-zero points (text)
                x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
                rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
                #cv2.imshow("Cropped", rect) # Show it
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                cv2.imwrite('/home/caratred/Downloads/test/aadharcrop/'+filename ,rect)
# img = cv2.imread("/home/caratred/Downloads/drivers/training/voterId/6.jpg") # Read in the image and convert to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
# coords = cv2.findNonZero(gray) # Find all non-zero points (text)
# x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
# rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
# #cv2.imshow("Cropped", rect) # Show it
# #cv2.waitKey(0)
# #cv2.destroyAllWindows()
# cv2.imwrite('/home/caratred/cropedImages/aadhar.jpeg',rect)
