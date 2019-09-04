import sys

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as im
from scipy.ndimage import interpolation as inter
import cv2

input_file = "/home/raghu/09:59:01.989966document.jpeg"

img = im.open(input_file)
img.show()
# convert to binary
wd, ht = img.size
pix = np.array(img.convert('L').getdata(), np.uint8)
bin_img = 1 - (pix.reshape((ht, wd)) / 255.0)
plt.imshow(bin_img, cmap='gray')
plt.savefig('binary.png')


def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score


delta = 1
limit = 5
angles = np.arange(-limit, limit+delta, delta)
scores = []
for angle in angles:
    hist, score = find_score(bin_img, angle)
    scores.append(score)

best_score = max(scores)
best_angle = angles[scores.index(best_score)]
print('Best angle: {}'.format(best_angle))

# correct skew
data = inter.rotate(img, best_angle, reshape=False, order=0)
img = im.fromarray((255 * data).astype("uint8"))#.convert("RGB")
# im2 = Image.new('RGBA', (20, 20))
img.save('skew_corrected.jpeg')
print("//..'")
image=cv2.imread('skew_corrected.jpeg')
image[np.where((image == [0,0,0]).all(axis = 2))] = [0,33,166]
# backtorgb = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
cv2.imwrite('skew_corrected1.jpeg',image)