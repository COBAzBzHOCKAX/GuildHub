from django.shortcuts import render  # noqa F401
from django.views.generic import ListView, DetailView

from .models import Ad


class AdBoardView(ListView):
    model = Ad
    ordering = '-date_published'
    template_name = 'ad_board/ad_board.html'
    context_object_name = 'ad_list'


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ad_board/ad_detail.html'
    context_object_name = 'ad'