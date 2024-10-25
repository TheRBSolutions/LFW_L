from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.CustomSignupView.as_view(), name='account_signup'),
    path('login/', views.CustomLoginView.as_view(), name='account_login'),
    path('logout/', views.CustomLogoutView.as_view(), name='account_logout'),
    path('profile/', views.ProfileView.as_view(), name='account_profile'),
]
