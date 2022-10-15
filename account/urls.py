from django.urls import path, include
from .views import RegisterView, LoginView, LogoutViews,ChangePasswordView , ProfileView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logouts/', LogoutViews.as_view(), name='logouts'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='_profile'),
]


