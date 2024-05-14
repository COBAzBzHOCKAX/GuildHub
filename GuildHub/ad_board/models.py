from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from config import settings


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'), help_text=_('Enter your title here'))
    text = models.TextField(verbose_name=_('Text'), help_text=_('Enter your text here'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    is_published = models.BooleanField(default=False, verbose_name=_('Is published'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_of_change = models.DateTimeField(auto_now=True, verbose_name=_('Date of change'))
    date_published = models.DateTimeField(null=True, blank=True, verbose_name=_('Date of publication'))

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.title

    def publish_ad(self):
        """
        Method to publish the advertisement.
        """
        self.is_published = True
        self.date_published = timezone.now()
        self.save()


class Category(models.Model):
    category_name = models.CharField(
        unique=True,
        max_length=255,
        verbose_name=_('Category name'),
        help_text=_('Enter your category name here'),
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')