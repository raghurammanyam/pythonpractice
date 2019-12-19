from collections import Counter
from matplotlib import pyplot as plt
import numpy as np
l = [('C16510', None), ('C16520', None), ('C16520', 30000), ('C16280', '896'),
     ('C16300', '524.3333333333'), ('C16310', '524.3333333333'), ('C16310', '12400')]

ctr = Counter(l)

results = {}                              
for k, v in ctr:                  
    results.setdefault(k, []).append(v)
print(results)
keys = [str(i) for i in results.keys()]
print(keys)

values = [i for i in results.values()]
#print(values, type(values[0]))
y = []
for i in values:
    x =np.array(i, dtype=np.float64)
    where_are_NaNs = np.isnan(x)
    x[where_are_NaNs] = 0
    print("cnmjdn",x)
    y.append(float(np.nanmax(x)))
print(y)


print(y)
fg = plt.figure(figsize=(15, 8), dpi=100)

plt.title("CSA LOAD HRS")
plt.show()

plt.bar(keys, y, label='site')