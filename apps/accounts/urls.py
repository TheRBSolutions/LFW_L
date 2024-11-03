# apps/accounts/urls.py
from django.urls import path, include
from . import views  # Import views for custom auth

urlpatterns = [
    path('signup/', views.signup_view, name='account_signup'),  # Custom signup
    path('login/', views.login_view, name='account_login'),  # Custom login
    path('logout/', views.logout_view, name='account_logout'),  # Custom logout
    
    # Include only the social account URLs for Google login
    path('', include('allauth.urls')),
    path('', include('allauth.socialaccount.urls')),
]
