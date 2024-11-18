# apps/accounts/urls.py
from django.urls import path, include
from . import views


urlpatterns = [
    # Basic authentication views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='account_logout'),
    path('register/', views.register_view, name='register'),
    # Password reset URLs
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset/sent/', views.password_reset_sent_view, name='password_reset_sent'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
    path('verify-email/<uidb64>/<token>/', views.verify_email_view, name='verify_email'),
    path('verify-device/<uidb64>/<token>/', views.verify_device_view, name='verify_device'),



]
