import slate
from slate import *

def extract_text_from_pdf(pdf_path):

    with open(pdf_path) as fh:

        document = slate.PDF(fh,  just_text=1)

    for page in document:

        print(page)

if __name__ == '__main__':

    extract_text_from_pdf('/home/caratred/Downloads/mrzlines.pdf')
