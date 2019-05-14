from PIL import Image

black = (0,0,0)
white = (255,255,255)
threshold = (160,160,160)

# Open input image in grayscale mode and get its pixels.
img = Image.open("/home/caratred/copy/passport/CHINTHAKA ISHAN_GALAPATHY_458.jpeg").convert("LA")
pixels = img.getdata()

newPixels = []

# Compare each pixel
for pixel in pixels:
    if pixel < threshold:
        newPixels.append(black)
    else:
        newPixels.append(white)

# Create and save new image.
newImg = Image.new("RGB",img.size)
newImg.putdata(newPixels)
newImg.save("/home/caratred/newImage.jpeg")
