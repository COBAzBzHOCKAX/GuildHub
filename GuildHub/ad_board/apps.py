from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ad_board'
    verbose_name = _('Ad boards')
