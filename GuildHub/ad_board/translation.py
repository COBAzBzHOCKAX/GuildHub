from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import Ad, Category


@register(Ad)
class AdTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)
