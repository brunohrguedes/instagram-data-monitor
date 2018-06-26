from apscheduler.schedulers.blocking import BlockingScheduler
import os
sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=23, minute=10)
def scheduled_job():
    print('Coletar stories e outros dados 11:10pm.')
    os.system("python main.py")

sched.start()
