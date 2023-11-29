#!/usr/bin/env python3

from collect_data import update_all
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()


@sched.scheduled_job('interval', hours=1)
def scheduled_collection():
    update_all()


sched.start()
