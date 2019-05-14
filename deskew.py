import cv2
import numpy as np

img = cv2.imread('/home/caratred/Downloads/test/aadhaar/2019-05-07 16:01:26.815372.jpg', cv2.IMREAD_GRAYSCALE)

def compute_skew(image):
    image = cv2.bitwise_not(image)
    height, width = image.shape
    # Filter removed
    # edges = cv2.Canny(image, 150, 200, 3, 5)
    lines = cv2.HoughLinesP(image, 1, np.pi/180, 100, minLineLength=width / 2.0, maxLineGap=20)
    angle = 0.0
    # lines.size gets the number of lines multiplied by 4 (number of columns)
    # nlines = lines.size
    # so now, I only use the number of lines
    nlines = lines.size
    # this reshape was necessary in order to convert the shape from (n_lines,1,4) to (n_lines,4)
    lines = lines.reshape(lines.shape[0], 4)
    # [0] removed because of the new shape
    # for x1, y1, x2, y2 in lines[0]:
    for x1, y1, x2, y2 in lines:
        angle += np.arctan2(y2 - y1, x2 - x1)

    # The function cv2.getRotationMatrix2D recieves as input the
    # angle in degrees, so I converted the return
    # https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#getrotationmatrix2d
    #return angle / nlines

    angle /= nlines
    return angle*180/np.pi


def deskew(image, angle):
    image = cv2.bitwise_not(image)
    non_zero_pixels = cv2.findNonZero(image)
    center, wh, theta = cv2.minAreaRect(non_zero_pixels)

    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    rows, cols = image.shape
    rotated = cv2.warpAffine(image, root_mat, (cols, rows), flags=cv2.INTER_CUBIC)

    return cv2.getRectSubPix(rotated, (cols, rows), center)


deskewed_image = deskew(img.copy(), compute_skew(img))

cv2.imshow('original', img)
cv2.imshow('deskew', deskewed_image)
cv2.waitKey(0)
