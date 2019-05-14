# Import PassportEye
from passporteye import read_mrz

# Process image
mrz = read_mrz("/home/caratred/copy/passports/ANDREY_SHAFIR_670.jpeg")
print(mrz)

# Obtain image
mrz_data = mrz.to_dict()
print(dict(mrz_data))
print(mrz_data['country'])
print(mrz_data['names'])
print(mrz_data['surname'])
print(mrz_data['type'])
# And so on with the rest of shown properties in the previous JSON string
