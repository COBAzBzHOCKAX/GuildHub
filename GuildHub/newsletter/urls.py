from django.urls import path

from newsletter.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, NewsletterDeleteView, \
    newsletter_publish, newsletter_unpublish

urlpatterns = [
    path('', NewsletterListView.as_view(), name='newsletters'),
    path('newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletter/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/update/<int:pk>/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter/delete/<int:pk>/', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletter/<int:pk>/publish/', newsletter_publish, name='newsletter_publish'),
    path('newsletter/<int:pk>/unpublish/', newsletter_unpublish, name='newsletter_unpublish'),
]
