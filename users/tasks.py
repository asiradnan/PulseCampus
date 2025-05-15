from celery import shared_task
from django.core.mail import send_mail

@shared_task
def test(arg):
    send_mail(
        'Test Email',
        'This is a test email sent from Celery.',
        'mail-pulsecampus@asiradnan.com',
        ['asir.adnan@g.bracu.ac.bd'],
        fail_silently=False,
    )