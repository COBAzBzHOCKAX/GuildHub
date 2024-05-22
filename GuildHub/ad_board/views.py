from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render  # noqa F401
from django.views.generic import ListView, DetailView, CreateView

from .filters import AdFilter
from .forms import AdForm
from .models import Ad

PAGINATE_BY = 2


class AdBoardView(ListView):
    model = Ad
    ordering = '-date_published'
    template_name = 'ad_board/ad_board.html'
    context_object_name = 'ad_list'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    form_class = AdForm
    model = Ad
    template_name = 'ad_board/ad_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ad_board/ad_detail.html'
    context_object_name = 'ad'
