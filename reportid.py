import requests
import json
import pandas as pd
from pprint import pprint

def reportid():
    final_data=[]
    params = {
        "grant_type": "password",
        "client_id": "3MVG99OxTyEMCQ3gUD3vF8Y8ie97jGc2iKs__OCuoUv6ecvrUVuAyOu_qsL2zsWTeLpVZYUGEQiPJU28CTa2r", # Consumer Key
        "client_secret": "70394CB345C56C6A42131237A4EB3FE2277EC90000CB9DCA04B2B18E0D434B19", # Consumer Secret
        "username": "ntt.data@doosan.com", # The email you use to login
        "password": "Nttdata@02CrYOI3DNa7j7Or1nbQsSvVyF" # Concat your password and your security token
    }
    r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
    print(r)


    reports_id = {
            "sd_data"   : "00O40000004ivdX",
            "work_order": "00O1W000004j57b",
            "Others"    : "00O1W000004jG1K"
    }
    access_token = r.json().get("access_token")
    instance_url = r.json().get("instance_url")
    print("Access Token:", access_token)
    print("Instance URL", instance_url)

    # Get Method
    for id in reports_id.values():
        end_uri = instance_url + "/services/data/v35.0/analytics/reports/"+str(id)+"?includeDetails=true"
        r=requests.get(end_uri, headers={"content-type" : "application/json", "Authorization" : "OAuth " + access_token})
        data = r.json()
        print(data)
        final_data.append(data)
    #print(final_data,"final_data")
    final_data = [x for x in final_data if type(x)!=list ]
   #s print(final_data)
    for x in final_data:
        with open ("/home/caratred/image/testfile.txt","w") as f:
            f.write(str(x))
        #print(x.keys())
        #abc =(x['factMap'])
        #print(abc)
        #df = pd.DataFrame(x)
        #print(df)



    return final_data
# multiple report ids mention below


reportid()
