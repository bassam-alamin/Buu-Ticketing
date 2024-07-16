from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth.models import User


@shared_task
def generate_weekly_report():
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        recent_users = User.objects.filter(date_joined__range=[start_date, end_date])
        # Todo: You can decide on the means to expose this infomation either email or pdf
        return recent_users.count()
    except Exception as error:
        print(error)
        return False