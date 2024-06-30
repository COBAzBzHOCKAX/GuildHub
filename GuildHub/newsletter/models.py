from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField

User = get_user_model()


class Newsletter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    title = models.CharField(max_length=255, verbose_name=_('Title'), help_text=_('Enter your title here'))
    text = QuillField(verbose_name=_('Text'), help_text=_('Enter your text here'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    is_published = models.BooleanField(default=False, verbose_name=_('Is published'))
    is_sent_email = models.BooleanField(
        default=False,
        verbose_name=_('Email sent'),
        help_text="Indicates whether the newsletter has been sent to users via email."
    )

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    def get_absolute_url(self):
        return reverse('newsletter_detail', kwargs={'pk': self.pk})

    def short_title(self):
        if len(self.title) > 50:
            return self.title[:50] + '...'
        return self.title

    def short_text(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        return self.text

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Newsletter.objects.get(pk=self.pk).is_published
            if self.is_published and not old_status:
                self.date_creation = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_title
