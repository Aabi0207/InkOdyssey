from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserDetailView,
    ChangePasswordView,
)

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # JWT token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Social authentication (django-allauth + dj-rest-auth)
    path('social/', include('dj_rest_auth.registration.urls')),
]
