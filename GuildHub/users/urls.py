from django.urls import path

from users.views import UserDetailView

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='profile'),
]