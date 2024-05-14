from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings


class Newsletter(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Author'))
    title = models.CharField(max_length=255, verbose_name=_('Title'), help_text=_('Enter your title here'))
    text = models.TextField(verbose_name=_('Text'), help_text=_('Enter your text here'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    is_published = models.BooleanField(default=False, verbose_name=_('Is published'))

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')