from ad_board.models import Ad
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
import django_filters

from .models import Response


User = get_user_model()


class ResponseFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=Response.ResponseStatusChoices.choices,
        label=_('Status'),
    )
    start_date_creation = django_filters.DateFilter(
        field_name='date_creation',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gte',
        label=_('Replied on start Date'),
    )
    end_date_creation = django_filters.DateFilter(
        field_name='date_creation',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='lte',
        label=_('Replied on end Date'),
    )
    ad_title = django_filters.ModelChoiceFilter(
        queryset=Ad.objects.none(),
        field_name='ad',
        label=_('Ad Title'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=_('All Ads'),
    )

    class Meta:
        model = Response
        fields = {
            'status': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ResponseFilter, self).__init__(*args, **kwargs)
        if self.user:
            self.filters['ad_title'].queryset = Ad.objects.filter(user=self.user)
