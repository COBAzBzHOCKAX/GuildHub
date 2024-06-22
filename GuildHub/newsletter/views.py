from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from users.mixins import StaffRequiredMixin, staff_required
from .forms import NewsletterForm
from .models import Newsletter


PAGINATE_BY = 10


class NewsletterListView(ListView):
    model = Newsletter
    context_object_name = 'newsletters'
    template_name = 'newsletter/newsletters.html'
    paginate_by = PAGINATE_BY
    ordering = '-date_creation'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Newsletter.objects.all().order_by('is_published', '-date_creation')
        return Newsletter.objects.filter(is_published=True).order_by('-date_creation')


class NewsletterDetailView(DetailView):
    model = Newsletter
    context_object_name = 'newsletter'
    template_name = 'newsletter/newsletter_detail.html'


class NewsletterCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_create.html'
    success_url = reverse_lazy('newsletters')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_update.html'


class NewsletterDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Newsletter
    context_object_name = 'newsletter'
    template_name = 'newsletter/newsletter_delete.html'


@login_required
@staff_required
def newsletter_publish(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.is_published = True
    newsletter.save()
    return redirect('newsletter_detail', pk=pk)

@login_required
@staff_required
def newsletter_unpublish(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.is_published = False
    newsletter.save()
    return redirect('newsletter_detail', pk=pk)
