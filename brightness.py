import os
import numpy as np
import cv2

folder = '/home/caratred/copy/passport/'

# We get all the image files from the source folder
files = list([os.path.join(folder, f) for f in os.listdir(folder)])

# We compute the average by adding up the images
# Start from an explicitly set as floating point, in order to force the
# conversion of the 8-bit values from the images, which would otherwise overflow
average = cv2.imread(files[0]).astype(np.float)
for file in files[1:]:
    dan =file.strip('/home/caratred/copy/passport/')
    #print("filename:",dan)
    image = cv2.imread(file)
    # NumPy adds two images element wise, so pixel by pixel / channel by channel
    average += image
    #print("average:",average)
    #average -= average_noise

# Divide by count (again each pixel/channel is divided)
    #print("length of files:",len(files))
    average /= len(files)

    # Normalize the image, to spread the pixel intensities across 0..255
    # This will brighten the image without losing information
    output = cv2.normalize(average, None, 0, 305, cv2.NORM_MINMAX)

    # Save the output
    cv2.imwrite('/home/caratred/bright/'+ dan, output)
