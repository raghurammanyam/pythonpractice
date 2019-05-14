from alyn.deskew import Deskew
d = Deskew(
	input_file='/home/caratred/Downloads/test/aadhaar/2019-05-07 16:01:25.844038.jpg',
	display_image='preview the image on screen',
	output_file='/home/caratred/skew.jpeg',
	r_angle=45,sigma='canny edge detection blurring')
d.run()
