from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # path('', name='home'),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('allauth.urls')),
    path('ad_board/', include('ad_board.urls')),
    path('', include('newsletter.urls')),
    path('profile/', include('users.urls')),
]
