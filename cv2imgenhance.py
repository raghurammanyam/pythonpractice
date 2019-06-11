import cv2
import pytesseract
from PIL import Image
image = cv2.imread("/home/caratred/Downloads/images/driving/15.JPG")
image_c = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale
cv2.imshow('gray', gray)
cv2.waitKey(0)

_, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # threshold
cv2.imshow('thresh', thresh)
cv2.waitKey(0)

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

dilated = cv2.dilate(thresh, kernel, iterations=1)  # dilate
cv2.imshow('dilated', dilated)
cv2.waitKey(0)

image, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

# for each contour found, draw a rectangle around it on original image
for i, contour in enumerate(contours):
    # get rectangle bounding contour
    x, y, w, h = cv2.boundingRect(contour)

    roi = image_c[y:y + h, x:x + w]

    if 50 < h < 100 or 200 < w < 420:  # these values are specific for this example

        # draw rectangle around contour on original image
        rect = cv2.rectangle(image_c, (x, y), (x + w, y + h), (255, 255, 255), 1)
        cv2.imshow('rectangles', rect)
        cv2.waitKey(0)

        cv2.imwrite('/home/caratred/sunset_modified1.jpeg', rect)
        text = pytesseract.image_to_string(Image.open('/home/caratred/sunset_modified1.jpeg'))
        print("text:",text)


# write original image with added contours to disk - change values above to (255,0,255) to see clearly the contours
cv2.imwrite("/home/caratred/sunset_modified2.jpeg", roi)
text = pytesseract.image_to_string(Image.open('/home/caratred/sunset_modified2.jpeg'))
print(":",text)
