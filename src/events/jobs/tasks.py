from celery import shared_task


@shared_task()
def celery_health_check(msg: str):
    """A task to check if celery is running"""
    print(msg)
    return msg
