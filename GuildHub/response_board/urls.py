from django.urls import path

from response_board.views import respond_to_ad, ResponseBoardView

urlpatterns = [
    path('respond/<int:pk>/', respond_to_ad, name='respond_to_ad'),
    path('', ResponseBoardView.as_view(), name='respond_board'),
]
