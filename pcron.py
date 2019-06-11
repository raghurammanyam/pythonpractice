from crontab import CronTab

cron = CronTab(user=True)

job1 = cron.new(command='python /home/caratred/image/pythonpractice/pnddb.py')

job1.minute.every(1)
job1.enable()



for item in cron:
    print(item)

cron.write()
