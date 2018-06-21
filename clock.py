from apscheduler.schedulers.blocking import BlockingScheduler
import os
sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=23)
def scheduled_job():
    print('Coletar stories e outros dados 11pm.')
    os.system("python src/main.py")
    os.system("python src/stories/stories.py")
    os.system("python src/stories/stories/cvt.py")

sched.start()