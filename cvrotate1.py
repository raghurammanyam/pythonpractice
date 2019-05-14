import cv2
import numpy as np

img = cv2.imread("/home/caratred/Downloads/drivers/paper_visas/AURORA_CHIAPPI_550_0.jpeg")  #load an image of a single battery
img_gs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert to grayscale

#inverted binary threshold: 1 for the battery, 0 for the background
_, thresh = cv2.threshold(img_gs, 250, 1, cv2.THRESH_BINARY_INV)

#From a matrix of pixels to a matrix of coordinates of non-black points.
#(note: mind the col/row order, pixels are accessed as [row, col]
#but when we draw, it's (x, y), so have to swap here or there)
mat = np.argwhere(thresh != 0)

#let's swap here... (e. g. [[row, col], ...] to [[col, row], ...])
mat[:, [0, 1]] = mat[:, [1, 0]]
#or we could've swapped at the end, when drawing
#(e. g. center[0], center[1] = center[1], center[0], same for endpoint1 and endpoint2),
#probably better performance-wise


mat = np.array(mat).astype(np.float32) #have to convert type for PCA

#mean (e. g. the geometrical center)
#and eigenvectors (e. g. directions of principal components)
m, e = cv2.PCACompute(mat, mean = np.array([]))

#now to draw: let's scale our primary axis by 100,
#and the secondary by 50

center = tuple(m[0])
endpoint1 = tuple(m[0] + e[0]*100)
endpoint2 = tuple(m[0] + e[1]*50)

red_color = (0, 0, 255)
cv2.circle(img, center, 5, red_color)
cv2.line(img, center, endpoint1, red_color)
cv2.line(img, center, endpoint2, red_color)
cv2.imshow("after",img)
cv2.waitKey(0)
cv2.imwrite("out.png", img)
