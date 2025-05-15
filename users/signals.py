from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
async def send_confirmation_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail(
            'Welcome to PulseCampus',
            'Thank you for registering on PulseCampus!',
            'verify-pulsecampus@asiradnan.com',
            [instance.email],
            fail_silently=False,
        )
        print("Email sent")

