from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .tasks import send_confirmation_email
from django.core import signing

@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
    if created and instance.email:
        token = signing.dumps(instance.email)
        instance.is_active = False
        instance.save()
        send_confirmation_email.delay(instance.email, token)

