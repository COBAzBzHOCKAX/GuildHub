from django.urls import path

from ad_board.views import AdBoardView, AdDetailView, AdCreateView, AdUpdateView, ad_publish, ad_unpublish, ad_delete, \
    MyAdsView

# URLs for ad_board/
urlpatterns = [
    path('', AdBoardView.as_view(), name='ad_board'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('create/', AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('<int:pk>/publish/', ad_publish, name='ad_publish'),
    path('<int:pk>/unpublish/', ad_unpublish, name='ad_unpublish'),
    path('<int:pk>/delete/', ad_delete, name='ad_delete'),
    path('my/', MyAdsView.as_view(), name='my_ads'),
]
