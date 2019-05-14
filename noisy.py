import cv2
# Load an color image in grayscale
img = cv2.imread('/home/caratred/Downloads/342i.jpeg',0)
ret, thresh_img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('grey image',thresh_img)
cv2.imwrite("/home/caratred/result11.jpg", thresh_img)
cv2.imshow("after threshold:",thresh_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
