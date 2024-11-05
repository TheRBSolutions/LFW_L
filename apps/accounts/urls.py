# apps/accounts/urls.py
from django.urls import path, include
from allauth.account.views import (
    LoginView, 
    SignupView, 
    LogoutView,
    EmailView,
    PasswordChangeView,
    PasswordResetView
)

urlpatterns = [
    # Basic authentication views
    path('login/', LoginView.as_view(), name='account_login'),
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    
    # Email management
    path('email/', EmailView.as_view(), name='account_email'),
    
    # Password management
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    
    # Include all remaining allauth URLs
    path('', include('allauth.account.urls')),
]