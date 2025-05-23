from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_confirmation_email(email_address, token):
    email_sent = send_mail(
            'Welcome to PulseCampus',
            'Thank you for registering on PulseCampus! Please verify your email address by clicking the link below: https://pulsecampus.asiradnan.com/users/verify_email/{} Note that the link is valid for 24 hours. '.format(token),
            'verify-pulsecampus@asiradnan.com',
            [email_address],
            fail_silently=False,
        )
    
@shared_task
def send_reset_email(email_address, token):
    email_sent = send_mail(
            'Password Reset',
            'Click the link below to reset your password: https://pulsecampus.asiradnan.com/users/reset_password/{}'.format(token),
            'verify-pulsecampus@asiradnan.com',
            [email_address],
            fail_silently=False
    )