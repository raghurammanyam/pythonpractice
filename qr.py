from pyzbar import pyzbar
import argparse
import cv2
from imutils import paths
import xmltodict
import pprint
import json
from collections import OrderedDict
import xml.etree.ElementTree
from lxml import etree
from lxml import objectify
from xml.etree import ElementTree
import xml.etree.ElementTree as ET

def qr_code(qr_code):
	image = cv2.imread(qr_code)
	barcodes = pyzbar.decode(image)
	#print("scannes_barcodes:",barcodes)
	for barcode in barcodes:

		(x, y, w, h) = barcode.rect
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 0, 255), 2)
		print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
		#cv2.imshow("Image", image)
		#cv2.waitKey(0)
		#tree = ElementTree.parse(barcodeData)
		#print("<>//////<>:",tree)
		pp = pprint.PrettyPrinter(indent=4)
		parser = etree.XMLParser(recover=True)
		print("parser_data:",parser)
	#	root=ET.fromstring.parser(str(barcodeData),encoding="utf-8")
		print("root_data:", str(barcodeData))
	#	data=etree.fromstring((barcodeData),parser=parser,encoding="utf-8")
	#	print("data:",data)
		#print(barcodeData.getValues("PrintLetterBarcodeData"))
		##pprint("acquired_data:",acquired_data)
	try:
		d=(xmltodict.parse(barcodeData,process_namespaces=True))
		print("person_data:",d)
		e=d['PrintLetterBarcodeData']
		person_aadhar_data=[]
		s = d.get('PrintLetterBarcodeData',)
		dit = dict(s)
		for x,y in dit.items():
			person_aadhar_data.append(y)
		print("person_aadhar_aadress:",person_aadhar_data)
	except xml.parsers.expat.ExpatError as ex:
		print(ex)
		#continue
qr_code("/home/caratred/Downloads/03092053209010.jpg")

#pp.pprint(json.dumps(xmltodict.parse(barcodeData)))
