from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ResponseBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'response_board'
    verbose_name = _('Response boards')

    def ready(self):
        from . import signals  # noqa F401
