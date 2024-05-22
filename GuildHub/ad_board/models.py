from django.urls import reverse

from config import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'), help_text=_('Enter your title here'))
    text = QuillField(verbose_name=_('Text'), help_text=_('Enter your text here'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    is_published = models.BooleanField(default=False, verbose_name=_('Is published'))
    date_published = models.DateTimeField(null=True, blank=True, verbose_name=_('Date of publication'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_of_change = models.DateTimeField(auto_now=True, verbose_name=_('Date of change'))

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

    def publish_ad(self):
        """Publish the advertisement."""
        self.is_published = True
        self.date_published = timezone.now()
        self.save()

    def unpublish_ad(self):
        """Unpublish the advertisement."""
        self.is_published = False
        self.date_published = None
        self.save()

    def short_title(self):
        """Return the first 50 characters of the title."""
        if len(self.title) > 50:
            return self.title[:50] + '...'
        return self.title

    def short_text(self):
        """Return the first 50 characters of the text."""
        if len(self.text) > 50:
            return self.text[:50] + '...'
        return self.text

    def date_of_publication(self):
        """Set publication date if published, else set to None."""
        if self.is_published and not self.date_published:
            self.date_published = timezone.now()
        else:
            self.date_published = None

    def save(self, *args, **kwargs):
        self.date_of_publication()
        super().save(*args, **kwargs)


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

    def __str__(self):
        return self.category_name
