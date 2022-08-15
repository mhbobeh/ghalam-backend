import os

from ghalam import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ghalam.settings')

from celery import Celery, shared_task
from api.services import OTPManager
from ghalam.environments import *
from django.core.mail import send_mail, send_mass_mail

app = Celery('tasks')
app.conf.broker_url=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BROKER}'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.result_expires = 180


@shared_task
def _send_otp(phone_number):
    otp = OTPManager(phone_number)
    otp.generate_save()
    otp.send()

def send_otp(phone_number):
    _send_otp.apply_async(args=(phone_number))


@shared_task
def _send_email(email, subject, message):
    send_mail(subject=subject, message=message, recipient_list=[email, ])

def send_email(email, subject, message):
    _send_email.apply_async(args=(email, subject, message)) 
     

@shared_task
def _send_mass_email(email_list, subject, message):
    data_tuple = (
        subject,
        message,
        settings.EMAIL_HOST_USER,
        email_list
    )
    send_mass_mail((data_tuple), fail_silently=False)

def send_mass_email(email_list, subject, message):
    _send_mass_email.apply_async(args=(email_list, subject, message))
