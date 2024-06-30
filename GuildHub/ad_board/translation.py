from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)
    required_languages = ('en', 'ru')
