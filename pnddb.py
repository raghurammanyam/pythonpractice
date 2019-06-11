
# import mysql.connector as sql
import MySQLdb
import pandas as pd
from flask import Flask
from flask_mail import Mail, Message
app =Flask(__name__)
db=MySQLdb.connect(host = '104.199.146.29', user = 'root', passwd = 'Welcome@123', db = 'scandetails')
cursor = db.cursor()
# db_connection = sql.connect(host='104.199.146.29', database='scandetails', user='root', password='Welcome@123')
# db_cursor = db_connection.cursor()
df = pd.read_sql('SELECT * FROM user', con=db)
#print(df)
# table_rows = df.fetchall()
# print(table_rows)

d = pd.DataFrame(df)
print(d.head())
app.app_context()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bhanuchander008@gmail.com'
app.config['MAIL_PASSWORD'] = 'abhi1015'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def index(subject, body):
   msg = Message(subject, sender = 'bhanuchander008@gmail.com', recipients = ['manyamraghuram@gmail.com'])
   msg.body = body
   mail.send(msg)
   return "Sent"
index("pandas data",str(d))
