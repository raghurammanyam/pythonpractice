from fpdf import FPDF
from tabula import read_pdf,wrapper
import pandas as pd


pdf = FPDF()

def pdfocr():
    #pdf.image(imgpath,x,y,w,h)
    #pdf.output("/home/caratred/text.pdf", "F")
    a=wrapper.read_pdf("/home/caratred/Downloads/mrzlines.pdf",pages="1",index=False,stream=True,squeeze=True,header=None)
    print(a)
    b=a.iloc[:,0:3]
    print(b)
pdfocr()
