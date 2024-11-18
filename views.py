from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomAdminLogoutView(LogoutView):
    next_page = reverse_lazy('admin:login')  # Redirect to admin login
