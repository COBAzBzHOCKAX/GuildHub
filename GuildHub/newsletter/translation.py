from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import Newsletter


@register(Newsletter)
class NewsletterTranslationOptions(TranslationOptions):
    fields = ('title', 'text')
