import datetime

from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import DateFilter, FilterSet, ModelMultipleChoiceFilter, NumberFilter

from .models import Ad, Category


class AdFilter(FilterSet):
    categories = ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label=_('Categories'),
    )

    start_date = DateFilter(
        field_name='date_published',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gte',
        label=_('Start Date'),
    )

    end_date = DateFilter(
        field_name='date_published',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='lte',
        label=_('End Date'),
    )

    min_age = NumberFilter(
        method='filter_by_min_age',
        label=_('Minimum Age'),
    )

    max_age = NumberFilter(
        method='filter_by_max_age',
        label=_('Maximum Age'),
    )

    class Meta:
        model = Ad
        fields = {
            'title': ['icontains'],
        }

    def filter_by_min_age(self, queryset, name, value):
        today = datetime.date.today()
        min_brith_year = today.year - value
        queryset = queryset.filter(user__date_birth__year__lt=min_brith_year)
        return queryset

    def filter_by_max_age(self, queryset, name, value):
        today = datetime.date.today()
        max_brith_year = today.year - value - 1
        queryset = queryset.filter(user__date_birth__year__gte=max_brith_year)
        return queryset


class MyAdsFilter(FilterSet):
    categories = ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label=_('Categories'),
    )

    start_date = DateFilter(
        field_name='date_published',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gte',
        label=_('Start Date'),
    )

    end_date = DateFilter(
        field_name='date_published',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='lte',
        label=_('End Date'),
    )

    class Meta:
        model = Ad
        fields = {
            'title': ['icontains'],
            'text': ['icontains'],
        }
