
import cv2


def threshold(im, method):
    # make it grayscale
    im_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    if method == 'fixed':
        threshed_im = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)

    elif method == 'mean':
        threshed_im = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)

    elif method == 'gaussian':
        threshed_im = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 7)

    else:
        return None

    return threshed_im


image = cv2.imread('/home/caratred/Downloads/3.png')

# threshold it
thresh = threshold(image, 'mean')

# find contours
_, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

#print len(cnts)

cv2.drawContours(image, cnts, -1, (0, 255, 0), 20)
cv2.imshow('contours', image)
cv2.imwrite("/home/caratred/ss3.jpg",image)
cv2.waitKey()

cv2.drawContours(thresh, cnts, -1, (0, 255, 0), 20)
cv2.imshow('contours', thresh)
cv2.imwrite("/home/caratred/ss3.jpg",thresh)
cv2.waitKey()
