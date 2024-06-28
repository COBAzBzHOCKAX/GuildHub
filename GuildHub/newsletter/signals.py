from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Newsletter
from .tasks import send_newsletter


@receiver(post_save, sender=Newsletter)
def publish_newsletter(sender, instance, created, **kwargs):
    if instance.is_published and not instance.is_sent_email:
        send_newsletter.delay(instance.pk)
