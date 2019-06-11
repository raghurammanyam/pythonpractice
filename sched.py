import schedule
import time
import smtplib
import os, sys
fpid = os.fork()
if fpid!=0:
  # Running as daemon now. PID is fpid
  sys.exit(0)

def job():
   print("I'm working...")

def send(mail_id):
   gmail_user = 'bhanuchander008@gmail.com'
   gmail_pwd = 'abhi1015'
   FROM = gmail_user
   recipient = mail_id
   TO = recipient if type(recipient) is list else [recipient]
   SUBJECT = 'User Registration'
   TEXT = 'succesfully registered as a user in our app'
   message = """From: %s\nTo: %s\nSubject: %s\n\n%s
   """% (FROM, ", ".join(TO), SUBJECT, TEXT)
   try:
       server = smtplib.SMTP("smtp.gmail.com", 587)
       server.ehlo()
       server.starttls()
       server.login(gmail_user, gmail_pwd)
       server.sendmail(FROM, TO, message)
       server.close()
       return ("success")
   except Exception as ex:
       return (ex)

schedule.every(1).minutes.do(send,mail_id='manyamraghuram@gmail.com')
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
while 1:
    while 1:
       schedule.run_pending()
       time.sleep(1)
    sleep(1)

# while 1:
#    schedule.run_pending()
#    time.sleep(1)
