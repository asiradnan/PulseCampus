from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_confirmation_email(email_address):
    send_mail(
            'Welcome to PulseCampus',
            'Thank you for registering on PulseCampus!',
            'verify-pulsecampus@asiradnan.com',
            [email_address],
            fail_silently=False,
        )