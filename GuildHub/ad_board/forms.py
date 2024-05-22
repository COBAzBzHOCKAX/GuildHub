from django import forms
from django_quill.fields import QuillField
from django.utils.translation import gettext_lazy as _

from .models import Ad, Category


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'text', 'category']

    title = forms.CharField(max_length=255, label=_('Title'), required=True, help_text=_('Enter your title here'))
    text = QuillField(verbose_name='Text', help_text=_('Enter your text here'))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label=_('Category'),
        help_text=_('Specify the ad category'),
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

    category_name = forms.CharField(
        max_length=255,
        label=_('Category name'),
        help_text=_('Enter your category name here'),
    )
