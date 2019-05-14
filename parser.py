from datetime import date, datetime


date = str(date.today())
last_two = date[0:4]

print("date:",date,last_two[2:4])
no=int(last_two[2:4])+1
birth='01/11/28'
fab=birth[0:2]
print(fab)
f = [str(x) for x in range(00,20)]
print(f)
parsed_list=[]
for y in f:
    if len(y)==1:
        abc =str(0)+y
        parsed_list.append(abc)
    else:
        parsed_list.append(y)
print(parsed_list)
if fab in parsed_list:
    print(fab)
    issue=str(20)+birth
    print("date_issue:",issue)
else:
    issue=str(19)+birth
    print("date_issue:",issue)
