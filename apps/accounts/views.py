# apps/accounts/views.py
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.urls import reverse
import os
from django.conf import settings
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, get_backends
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .forms import RegistrationForm



import logging
logger = logging.getLogger('apps.accounts')  # Use 'apps.accounts' to match your LOGGING config



User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Add debug logging
        logger.debug(f"Login attempt for email: {email}")
        
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user is not None:
                # First, ensure trusted_devices exists and is a list
                if not hasattr(user, 'trusted_devices') or user.trusted_devices is None:
                    user.trusted_devices = []
                    user.save()
                
                # Get or generate device_id
                device_id = request.COOKIES.get('device_id')
                logger.debug(f"Existing device_id from cookies: {device_id}")
                
                if not device_id:
                    device_id = get_random_string(15)
                    logger.debug(f"Generated new device_id: {device_id}")
                
                # Debug log the trusted devices
                logger.debug(f"User's trusted devices: {user.trusted_devices}")
                logger.debug(f"Current device_id: {device_id}")
                
                # Check if device is trusted
                trusted_device = device_id in user.trusted_devices
                logger.debug(f"Is device trusted? {trusted_device}")

                if not trusted_device:
                    logger.debug("Device not trusted, sending verification email")
                    # Generate verification token
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    
                    # Set the temporary device_id cookie before redirect
                    response = redirect('login')
                    response.set_cookie('device_id', device_id, max_age=30*24*60*60)
                    
                    # Build verification URL
                    domain = request.get_host()
                    scheme = 'https' if request.is_secure() else 'http'
                    verification_url = f"{scheme}://{domain}/accounts/verify-device/{uid}/{token}/"
                    
                    # Send verification email
                    email_context = {
                        'user': user,
                        'verification_url': verification_url,
                        'site_name': domain,
                    }
                    email_body = render_to_string('accounts/device_verification.html', email_context)
                    
                    send_mail(
                        'Verify Device Login',
                        email_body,
                        'therbsol@therbsolutions.com',
                        [user.email],
                        fail_silently=False,
                    )
                    
                    messages.info(request, 'Please check your email to verify this device before logging in.')
                    return response
                
                # Device is trusted, proceed with login
                logger.debug("Device is trusted, proceeding with login")
                login(request, authenticated_user)
                
                # Ensure device_id is in trusted_devices
                if device_id not in user.trusted_devices:
                    user.trusted_devices.append(device_id)
                    user.save()
                    logger.debug(f"Added device_id to trusted devices: {user.trusted_devices}")
                
                # Set cookie and redirect
                response = redirect('home')
                response.set_cookie('device_id', device_id, max_age=30*24*60*60)
                return response
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        # Log the received POST data (excluding sensitive information)
        sanitized_post_data = request.POST.copy()
        sanitized_fields = ['password', 'password_confirmation', 'password1', 'password2']
        for field in sanitized_fields:
            if field in sanitized_post_data:
                sanitized_post_data[field] = '****'
        logger.debug("Received POST data: %s", sanitized_post_data)

        form = RegistrationForm(request.POST)
        if form.is_valid():
            logger.info("Form is valid.")
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            logger.info("User created: %s", user)

            # Send verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            verification_url = request.build_absolute_uri(
                reverse('verify_email', args=[uid, token])
            )

            email_context = {
                'user': user,
                'verification_url': verification_url,
                'site_name': current_site.name,
            }
            email_body = render_to_string('accounts/email_verification.html', email_context)

            logger.debug("Sending email to: %s", user.email)
            try:
                send_mail(
                    'Verify Your Account',
                    email_body,
                    'therbsol@therbsolutions.com',  # Replace with your email
                    [user.email],
                    fail_silently=False,
                )
                logger.info("Verification email sent successfully to %s.", user.email)
            except Exception as e:
                logger.error("Error sending email to %s: %s", user.email, e)

            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect('login')
        else:
            logger.warning("Form is invalid: %s", form.errors.as_json())
            for field, errors in form.errors.items():
                logger.debug("Field error - %s: %s", field, errors)
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

    

    
def verify_device_view(request, uidb64, token):
    try:
        # Step 1: Decode the UID
        uid = force_str(urlsafe_base64_decode(uidb64))
        logger.debug(f"Decoded UID: {uid}")

        # Step 2: Retrieve the User
        user_exists = User.objects.filter(pk=uid).exists()
        logger.debug(f"User exists: {user_exists}")

        if not user_exists:
            messages.error(request, 'The device verification link is invalid.')
            return redirect('login')

        user = User.objects.get(pk=uid)

        # Step 3: Validate the Token
        token_valid = default_token_generator.check_token(user, token)
        logger.debug(f"Token validation result: {token_valid}")

        if token_valid:
            # Mark device as trusted
            device_id = request.COOKIES.get('device_id', get_random_string(15))
            if device_id not in user.trusted_devices:
                user.trusted_devices.append(device_id)
                user.save()

            # Log the user in to establish an authenticated session
            backends = get_backends()
            user.backend = f"{backends[0].__module__}.{backends[0].__class__.__name__}"  # Select the appropriate backend
            login(request, user)
            login(request, user)
            messages.success(request, 'Device has been verified, and you are now logged in.')
            return redirect('home')  # Redirect to a desired page
        else:
            messages.error(request, 'The device verification link is invalid.')
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        logger.error(f"Error during verification: {e}")
        messages.error(request, 'The device verification link is invalid.')
        return redirect('login')

def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            user.is_active = True  # Activate user account
            user.save()
            messages.success(request, 'Your account has been verified! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'The verification link is invalid.')
            return redirect('register')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'The verification link is invalid.')
        return redirect('register')


def home_view(request):
    """
    Home page view that handles both authenticated and non-authenticated users.
    """
    if request.user.is_authenticated:
        return render(request, 'home.html', {
            'user': request.user
        })
    else:
        # Log that the user is not authenticated
        logger.info('User is not authenticated. Rendering registration form.')
        
        # If user is not authenticated, show the registration form
        form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})



def password_reset_view(request):
    """View to handle password reset request"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate token and UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build reset URL
            current_site = get_current_site(request)
            reset_url = f"{current_site.domain}/accounts/reset/{uid}/{token}/"

            # Email context
            context = {
                'user': user,
                'reset_url': reset_url,
                'site_name': current_site.name,
            }

            # Send email
            email_body = render_to_string('accounts/password_reset_email.html', context)
            send_mail(
                'Password Reset Request',
                email_body,
                'therbsol@therbsolutions.com',
                [user.email],
                fail_silently=False,
            )

            return redirect('password_reset_sent')
        except User.DoesNotExist:
            messages.error(request, "No user found with that email address.")

    return render(request, 'accounts/password_reset.html')

def password_reset_sent_view(request):
    """Confirmation page after reset email is sent"""
    return render(request, 'accounts/password_reset_sent.html')

def password_reset_confirm_view(request, uidb64, token):
    """View to handle password reset confirmation"""
    try:
        # Decode the user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Verify token
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                # Get new password
                new_password = request.POST.get('new_password1')
                confirm_password = request.POST.get('new_password2')

                if new_password == confirm_password:
                    # Set new password
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password has been reset successfully!')
                    return redirect('password_reset_complete')
                else:
                    messages.error(request, "Passwords don't match!")

            return render(request, 'accounts/password_reset_confirm.html')
        else:
            messages.error(request, 'Reset link is invalid!')
            return redirect('password_reset')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Reset link is invalid!')
        return redirect('password_reset')

def password_reset_complete_view(request):
    """Success page after password is reset"""
    return render(request, 'accounts/password_reset_complete.html')
