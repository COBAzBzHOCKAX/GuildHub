import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Response
from .tasks import send_ad_response_notification, send_response_accepted_notification


@receiver(post_save, sender=Response)
def create_response(sender, instance, created, **kwargs):
    logger = logging.getLogger('response_board.signals.create_response')
    logger.debug(f'launching. created = {created}')

    if created:
        # Send notification
        send_ad_response_notification.delay(instance.pk)
    else:
        logger.debug(f'Response with ID {instance.pk} already exists.')


@receiver(pre_save, sender=Response)
def update_response(sender, instance, **kwargs):
    logger = logging.getLogger('response_board.signals.update_response')
    logger.debug(f'launching. instance.pk = {instance.pk}')

    try:
        old_status = Response.objects.get(pk=instance.pk).status
    except Response.DoesNotExist:
        logger.error(f'Response with ID {instance.pk} does not exist.')
        return

    # Send notification if status changed to 'ACC'
    if old_status != instance.status and instance.status == 'ACC':
        send_response_accepted_notification.delay(instance.pk)

    logger.debug(f'Response with ID {instance.pk} was updated.')
