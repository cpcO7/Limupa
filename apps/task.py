import time

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from apps.models import User


@shared_task
def send_to_user_email(email: str, message: str):
    print(email, message)
    send_mail('Confirmation', message, settings.EMAIL_HOST_USER, [email])
    return f'send email to {email} successfully'


@shared_task
def send_to_all_email():
    user_emails = User.objects.values_list('email', flat=True)
    send_mail('Confirmation', 'DNX', settings.EMAIL_HOST_USER, user_emails)

    return f'send email to all users successfully'


@shared_task
def add(x, y):
    time.sleep(5)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
