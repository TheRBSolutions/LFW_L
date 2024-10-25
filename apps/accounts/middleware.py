# apps/accounts/middleware.py
import logging
from django.utils import timezone
from .models import UserActivity

logger = logging.getLogger(__name__)

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            try:
                UserActivity.objects.update_or_create(
                    user=request.user,
                    defaults={
                        'last_activity': timezone.now(),
                        'ip_address': self.get_client_ip(request),
                        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    }
                )
                logger.debug(f'Updated activity for user {request.user.email} from IP {self.get_client_ip(request)}')
            except Exception as e:
                logger.error(f'Error updating user activity for {request.user.email}: {str(e)}')
                logger.exception("Full traceback:")  # This will log the full traceback
        
        return response