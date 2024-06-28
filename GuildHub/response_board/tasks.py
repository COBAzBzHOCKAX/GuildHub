import logging
from celery import shared_task
from django.utils.translation import gettext_lazy as _

from common.utils import send_email
from .models import Response

logger = logging.getLogger('response_board.tasks')


@shared_task
def send_ad_response_notification(response_pk):
    logger.debug(f'Launching send_ad_response_notification. response_pk = {response_pk}')

    try:
        response = Response.objects.select_related('author', 'ad', 'ad__user').get(pk=response_pk)
    except Response.DoesNotExist:
        logger.error(f'Response with ID {response_pk} does not exist.')
        return

    email = response.ad.user.email
    title_ad = response.ad.short_title()
    nickname_responded = response.author.nickname
    response_text = response.short_text()

    subject = _(f'New response for your ad: {title_ad}.')
    text_content = _('To your ad "{title_ad}", the user {nickname_responded} made a response, with the text: "{response_text}".')
    html_content = _('<p>To your ad "{title_ad}", the user {nickname_responded} made a response, with the text: "{response_text}".</p>')

    text_content_formatted = text_content.format(
        title_ad=title_ad,
        nickname_responded=nickname_responded,
        response_text=response_text
    )
    html_content_formatted = html_content.format(
        title_ad=title_ad,
        nickname_responded=nickname_responded,
        response_text=response_text
    )

    send_email(subject, text_content_formatted, html_content_formatted, [email])

    logger.debug(f'Email sent to {email}.')


@shared_task
def send_response_accepted_notification(response_pk):
    logger.debug(f'Launching send_response_accepted_notification. response_pk = {response_pk}')

    try:
        response = Response.objects.select_related('author', 'ad', 'ad__user').get(pk=response_pk)
    except Response.DoesNotExist:
        logger.error(f'Response with ID {response_pk} does not exist.')
        return

    email = response.author.email
    response_text = response.short_text()
    ad_title = response.ad.short_title()

    subject = _('Your response has been accepted')
    text_content = _('Your response "{response_text}" to the ad "{ad_title}" has been accepted.')
    html_content = _('<p>Your response "{response_text}" to the ad "{ad_title}" has been accepted.</p>')

    text_content_formatted = text_content.format(response_text=response_text, ad_title=ad_title)
    html_content_formatted = html_content.format(response_text=response_text, ad_title=ad_title)

    send_email(subject, text_content_formatted, html_content_formatted, [email])

    logger.debug(f'Email sent to {email}.')
