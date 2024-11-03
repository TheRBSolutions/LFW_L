# apps/accounts/views.py
from allauth.account.views import SignupView as AllauthSignupView, LoginView as AllauthLoginView, LogoutView as AllauthLogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import logging
from django.shortcuts import render

# apps/accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomSignupForm, CustomLoginForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())  # Log the user in
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# Profile View
@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        logger.debug("ProfileView: Fetching context data for user profile.")
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# Custom Logout View using Allauth
# class CustomLogoutView(AllauthLogoutView):
#     next_page = 'account_login'



def home_view(request):
    return render(request, 'home.html')  # Make sure the template path is correct