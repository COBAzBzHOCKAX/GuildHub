from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from django.utils.translation import gettext_lazy as _

from .models import Ad, Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)
    required_languages = ('en', 'ru')
