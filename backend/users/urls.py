from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='token-obtain-pair'), # For obtaining token
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'), # For refreshing token
    path('me/', UserDetailView.as_view(), name='user-me'),
]
