from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings


class Response(models.Model):
    class ResponseStatusChoices(models.TextChoices):
        PENDING = 'PEN', _('Pending')
        ACCEPTED = 'ACC', _('Accepted')
        DECLINED = 'DEC', _('Declined')

    status = models.CharField(
        max_length=3,
        choices=ResponseStatusChoices.choices,
        default=ResponseStatusChoices.PENDING,
        verbose_name=_('Status'),
        help_text=_('Shows the current status of this request'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Author'))
    ad = models.ForeignKey('ad_board.Ad', on_delete=models.CASCADE, verbose_name=_('Ad'))
    text = models.TextField(verbose_name=_('Text'), help_text=_('Enter your text here'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_of_change = models.DateTimeField(auto_now=True, verbose_name=_('Date of change'))
    date_status_change = models.DateTimeField(null=True, blank=True, verbose_name=_('Date of status change'))

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['ad']),
        ]