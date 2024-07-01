from django.urls import path

from users.views import UserDetailView, UserUpdateView, UserDeactivateView

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='profile_update'),
    path('<int:pk>/deactivate/', UserDeactivateView.as_view(), name='profile_deactivate_url')
]
