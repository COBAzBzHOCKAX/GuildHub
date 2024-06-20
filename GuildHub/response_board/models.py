from django.core.validators import MaxLengthValidator
from django.utils import timezone

from chats.models import Chat, Message
from config import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    text = models.TextField(
        verbose_name=_('Text'),
        help_text=_('Enter your text here (1000 characters max)'),
        validators=[MaxLengthValidator(1000)]
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_of_change = models.DateTimeField(auto_now=True, verbose_name=_('Date of change'))
    date_status_change = models.DateTimeField(auto_now=True, verbose_name=_('Date of status change'))

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['ad']),
        ]

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_status = Response.objects.get(pk=self.pk).status
            if old_status != self.status:
                self.date_status_change = timezone.now()

        super().save(*args, **kwargs)

    def short_text(self):
        return self.text[:50]

    def __str__(self):
        return f'{self.author} - {self.short_text}'
