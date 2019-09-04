import json, re, subprocess
import pandas as pd
from pandas.compat import StringIO
import io
pdfname = '/home/raghu/Downloads/Down-Payment/Florida.pdf'

output = subprocess.check_output(
   ['pdftotext', '-layout', pdfname, '-']).decode()
print(output)
df = pd.read_fwf(data=io.StringIO(output),sep='\n')
print(df)

# import pdftotext

# # Load your PDF
# # with open("/home/raghu/Downloads/Down-Payment/Florida.pdf", "rb") as f:
# #     pdf = pdftotext.PDF(f).decode('utf-8')
# # print(pdf)
# import pandas as pd
# import rossum

# pdfname = rosuum.extract('/home/raghu/Downloads/Down-Payment/Florida.pdf')
# print(pdfname)