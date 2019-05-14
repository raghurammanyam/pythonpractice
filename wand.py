from PIL import Image, ImageEnhance,ImageFilter
import pytesseract

image = Image.open('/home/caratred/Downloads/drivers/mrz1.jpeg')#.convert('L')
image = image.filter(ImageFilter.SHARPEN())
scale_value=3.
#image = ImageEnhance.Contrast(image).enhance(scale_value)s
image=ImageEnhance.Contrast(image).enhance(1.8)
nx, ny = image.size
print("imagesize:",nx,ny)
img = image.resize((int(nx*1.5), int(ny*1.5)), Image.ANTIALIAS)
img.show()
img.save("/home/caratred/savepng.jpeg",quality=94)

im=Image.open("/home/caratred/savepng.jpeg")
im = im.convert('L')
for i in range(2,im.size[0]-2):
    for j in range(2,im.size[1]-2):
        b=[]
        if im.getpixel((i,j))>0 and im.getpixel((i,j))<255:
            pass
        elif im.getpixel((i,j))==0 or im.getpixel((i,j))==255:
            c=0
            for p in range(i-1,i+2):
                for q in range(j-1,j+2):
                    if im.getpixel((p,q))==0 or im.getpixel((p,q))==255: 
                        c=c+1
            if c>6:
                c=0
                for p in range(i-2,i+3):
                    for q in range(j-2,j+3):
                        b.append(im.getpixel((p,q)))
                        if im.getpixel((p,q))==0 or im.getpixel((p,q))==255:
                            c=c+1
                if c==25:
                    a=sum(b)/25
                    print (a)
                    im.putpixel((i,j),a)
                else:
                    p=[]
                    for t in b:
                        if t not in (0,255):
                            p.append(t)
                    p.sort()
                    im.putpixel((i,j),p[len(p)/2])
            else:
                b1=[]
                for p in range(i-1,i+2):
                    for q in range(j-1,j+2):
                        b1.append(im.getpixel((p,q)))
                print("n.../:",b1)
                a=i
                b=j   
                print("values of i,j:",i,j)     
                im.putpixel(tuple(a),tuple(b),sum(b1)/9)
im.save("/home/caratred/savepng.jpeg")   
text = pytesseract.image_to_string(Image.open('/home/caratred/savepng.jpeg').convert('L'))
print("text:",text)
