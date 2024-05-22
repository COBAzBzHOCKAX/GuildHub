from django.urls import path

from ad_board.views import AdBoardView, AdDetailView, AdCreateView

urlpatterns = [
    path('', AdBoardView.as_view(), name='ad_board'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('create/', AdCreateView.as_view(), name='ad_create'),
]
