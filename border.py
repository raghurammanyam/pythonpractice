# from PIL import Image
#
# img = Image.open('/home/caratred/Downloads/votecard/voter3.JPG')
# nonwhite_positions = [(x,y) for x in range(img.size[0]) for y in range(img.size[1]) if img.getdata()[x+y*img.size[0]] != (255,255,255)]
# rect = (min([x for x,y in nonwhite_positions]), min([y for x,y in nonwhite_positions]), max([x for x,y in nonwhite_positions]), max([y for x,y in nonwhite_positions]))
# img.crop(rect).save('/home/caratred/border.jpeg')


import cv2

BLACK_THRESHOLD = 200
THIN_THRESHOLD = 10
ANNOTATION_COLOUR = (222,0,222)

img = cv2.imread('/home/caratred/Downloads/votecard/voter3.JPG')
orig = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, thresh=BLACK_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY_INV)[1]

# Optional: save thesholded image
cv2.imwrite("temp_thres.png", thresh)

# Find contours on the thresholded image
contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
for cont in contours:
    # Find bounding rectangle of a contour
    x,y,w,h = cv2.boundingRect(cont)
    # Skip thin contours (vertical and horizontal lines)
    if h<THIN_THRESHOLD or w<THIN_THRESHOLD:
        continue
    # Does the countour has the right shape (roughly four times longer than high)?
    if 3*h<w<5*h:
        roi = orig[y:y+h,x:x+w]
        cv2.imwrite("/home/caratred/four_letters.jpeg",roi)

    # Optional: draw annotations
    cv2.rectangle(img,(x,y),(x+w,y+h),ANNOTATION_COLOUR,3)

# Optional: save annotated image
cv2.imwrite("/home/caratred/border.jpeg",img)
