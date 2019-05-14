import random
import cv2
import sys
import os
#from hurry.filesize import size

CASCADE="Face_cascade.xml"
FACE_CASCADE=cv2.CascadeClassifier(CASCADE)
rand_int=random.randint(0,10000)
def detect_faces(image_path):
#/home/caratred/image/Extracted
	image=cv2.imread(image_path)
	#print("image read:",image)
	image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	can=[]

	faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.16,minNeighbors=5,minSize=(40,50),flags=0)
	#print("found faces:",faces[0])
	found_face=faces[0]
	for x,y,w,h in faces:
		sub_img=image[y-20:y+h+65,x-10:x+w+25]
		os.chdir("Extracted")
		cv2.imwrite('/home/caratred/image/Extracted/'+str(rand_int)+".jpg",sub_img)
		os.chdir("../")
		cv2.rectangle(image,(x,y),(x+w,y+h),(255, 255,0),2)
		can.append(sub_img)
		break
	#can.append()
	#print("faces found:",can)
	#cv2.imwrite(str(rand_int)+".jpg",sub_img)
	path='/home/caratred/image/Extracted/'+str(rand_int)+'.jpg'
	#cv2.imshow("Faces Found",image)
	cv2.waitKey(0)
	import numpy as np
	image = cv2.imread(path)
	#height = np.size(image, 0)
	#width = np.size(image, 1)
	#print("height-width:",height,width)
	#print("imagepath:",rand_int)
	#image_size=os.path.getsize(path)
#	print(image_size)
	#size= ('{:,.0f}'.format(os.path.getsize(path)/float(1<<10))+" KB")
	#print("////////:",size)
	return path
	#if (cv2.waitKey(0) & 0xFF == ord('q')) or (cv2.waitKey(0) & 0xFF == ord('Q')):
		#cv2.destroyAllWindows()
#detect_faces('/home/caratred/copy/passport/ARTITTAYA_KERDPRAD_201.jpeg')


#detect_faces('/home/caratred/image/passports/Ukraine.png')
