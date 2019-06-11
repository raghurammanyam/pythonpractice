import requests
import json
from simple_salesforce import Salesforce
#from IPython.core import logger
#from rest_framework import generics
#from django.db import models

import psycopg2
#from salesforce_doosan.serializer import sd_Serializer
from urllib.parse import urlparse
#import urllib.parse


class Transform(object):

    def __init__(self,data):
        try:
            self.table_fields = data[0]['reportMetadata']['detailColumns']
        except:
            self.table_fields = None
        if self.table_fields:
            self.data = data[0]['factMap']['T!T']['rows']


    def data_dict(self):
        out = []
        for data in self.data:
            out.append({field:doc['label'] for field, doc in zip(self.table_fields,data['dataCells'])})
        return out
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

    #sf = Salesforce.query_more('00O40000004ivdX')
    #sf = Salesforce.query_more("/services/data/v35.0/analytics/reports/query/reports_id", True)
    # Get Method

    result = urlparse("postgresql://postgres:postgres@localhost/postgres")
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    conn = psycopg2.connect(
	    database = 'Sd-mod',
	    user = 'postgres',
	    password = 'Doosan@123',
	    host = 'localhost'
	)
	cur = conn.cursor()
    for id in reports_id.values():
        end_uri = instance_url + "/services/data/v35.0/analytics/reports/"+str(id)+"?includeDetails=true"
        r=requests.get(end_uri, headers={"content-type" : "application/json", \
                                         "Authorization" : "OAuth " + access_token,

                                         })
        json_data = r.json()
	    a = Transform(json_data).data_dict()
	    if id == "00O40000004ivdX":
    		cur.execute("Truncate data.sd_demo;")
    		cur.executemany("""INSERT INTO data."sd_demo"("shutdown_date_time", "owner", "fk_name", "case_number", "shutdown_alarm", 			"outage_type", "type", "load_hours_at_time_of_shutdown", "restart_date_time", "root_cause", "subject", "open", "closed", 			"resolution", "description") VALUES (%(Shutdown_Case_Details__c.Shutdown_Date_Time__c)s, %(OWNER)s, %(FK_NAME)s, %(CASE_NUMBER)s, %(Case.Shutdown_Alarm__c)s, %(Case.Outage_Type__c)s, %(TYPE)s, %(Case.Load_Hours_at_Time_of_Shutdown__c)s, %(Shutdown_Case_Details__c.Restart_Date_Time__c)s, %(Case.Root_Cause__c)s, %(SUBJECT)s, %(OPEN)s, %(CLOSED)s, %(Case.Resolution__c)s, %(DESCRIPTION)s)""", a)
    		cur.close()
    		conn.commit()
    		conn.close()
        elif id == "00O1W000004j57b":
            pass
        elif id == "00O1W000004jG1K":
            pass

        final_data.append(json_data)

        #print(final_data)
    return final_data

# multiple report ids mention below
x = reportid()
