import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from common.utils import send_email
from .models import Newsletter

User = get_user_model()


@shared_task
def send_newsletter(newsletter_pk):
    logger = logging.getLogger('newsletter.tasks.send_newsletter')
    logger.debug(f'Launching. newsletter_pk = {newsletter_pk}')

    try:
        newsletter = Newsletter.objects.get(pk=newsletter_pk)
    except Newsletter.DoesNotExist:
        logger.error(f'Newsletter with ID {newsletter_pk} does not exist.')
        return

    subject = (_('Guild Hub (Newsletter) - {}')).format(newsletter.short_title())
    text_content = render_to_string(
        'newsletter/email/send_newsletter.txt',
        {'newsletter': newsletter}
    )
    html_content = render_to_string(
        'newsletter/email/send_newsletter.html',
        {'newsletter': newsletter}
    )

    users = User.objects.filter(is_active=True)
    logger.info('Starting sending emails...')

    for user in users:
        send_email(subject, text_content, html_content, [user.email])

    logger.debug(f'Emails sent to {users.count()} users.')

    newsletter.is_sent_email = True
    newsletter.save()
    logger.debug('Newsletter is_sent_email = True')
    logger.debug('Finished.')
