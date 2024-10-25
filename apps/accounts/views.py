# apps/accounts/views.py

from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SignupForm
from django.urls import reverse_lazy
from allauth.account.views import SignupView as AllauthSignupView, LoginView as AllauthLoginView, LogoutView as AllauthLogoutView
import logging
from ninja import Router
from .models import User
from .serializers import UserSchema
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

# Custom User Signup View using Allauth
class CustomSignupView(AllauthSignupView):
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        logger.debug("CustomSignupView: Form is valid. Saving user.")
        return super().form_valid(form)

# Custom User Login View using Allauth
class CustomLoginView(AllauthLoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        logger.debug(f"CustomLoginView: User {form.cleaned_data.get('login')} is attempting to log in.")
        return super().form_valid(form)

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
class CustomLogoutView(AllauthLogoutView):
    next_page = 'account_login'

# Router Setup for Ninja
router = Router()

# List Users Endpoint
@router.get('/users', response=list[UserSchema])
def list_users(request):
    logger.debug("Fetching all users")
    return User.objects.all()

# Create User Endpoint
@router.post('/users', response=UserSchema)
def create_user(request, user: UserSchema):
    logger.debug(f"Creating user with data: {user}")
    user_instance = User.objects.create(**user.dict())
    return user_instance




def home_view(request):
    # If the user is not authenticated, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect('account_login')  # Redirect to the login page

    # If the user is authenticated, render the home page with links
    return render(request, 'home.html')
