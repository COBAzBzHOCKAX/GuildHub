from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import Response


@register(Response)
class ResponseTranslationOptions(TranslationOptions):
    fields = ('text',)
