from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter'
    verbose_name = _('Newsletters')

    def ready(self):
        from . import signals  # noqa F401
