from celery import shared_task

from main.business_logic.update_time import daily_update


@shared_task(name="daily_update")
def celery_update():
    print("DAILY UPDATE STARTED")
    daily_update()
    print("DAILY UPDATE ENDED")
