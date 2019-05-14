import dlib
from PIL import Image
from skimage import io
import matplotlib.pyplot as plt


def detect_faces():

    # Create a face detector
    face_detector = dlib.get_frontal_face_detector()

    # Run detector and get bounding boxes of the faces on image.
    detected_faces = face_detector(image, 1)
    face_frames = [(x.left(), x.top(),
                    x.right(), x.bottom()) for x in detected_faces]
    print(face_frames)
    return face_frames

# Load image
img_path = '/home/caratred/image/Canada.png'
image = io.imread(img_path)

# Detect faces
detected_faces = detect_faces()

# Crop faces and plot
for n, face_rect in enumerate(detected_faces):
    face = Image.fromarray(image).crop(face_rect)
    print(face)
    print(plt.subplot(1, len(detected_faces), n+1))
    print(plt.axis('on'))
    print(plt.imshow(face))
