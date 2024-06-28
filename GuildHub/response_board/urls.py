from django.urls import path

from .views import respond_to_ad, ResponseBoardView, accept_response, decline_response, MyResponsesView

# URLs for response_board/
urlpatterns = [
    path('respond/<int:pk>/', respond_to_ad, name='respond_to_ad'),  # Creates a response to an ad
    path('', ResponseBoardView.as_view(), name='respond_board'),  # Shows the response board
    path('my_responses/', MyResponsesView.as_view(), name='my_responses'),  # Shows the response board
    path('accept_response/<int:pk>/', accept_response, name='accept_response'),  # Accepts a response
    path('decline_response/<int:pk>/', decline_response, name='decline_response'),  # Declines a response
]
