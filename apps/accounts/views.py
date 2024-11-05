# apps/accounts/views.py
from allauth.account.views import SignupView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomSignupForm

class CustomSignupView(SignupView):
    template_name = 'accounts/signup.html'
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context you need
        return context

    def form_valid(self, form):
        # Custom logic before saving the user
        response = super().form_valid(form)
        # Custom logic after saving the user
        return response

def home_view(request):
    # Your home view logic here
    return render(request, 'home.html')

def profile_view(request):
    # Your profile view logic here
    return render(request, 'accounts/profile.html', {'user': request.user})