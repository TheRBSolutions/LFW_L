# apps/dashbord/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from apps.family_legacy.models import FamilyLegacy
from apps.content.models import Content
from apps.accounts.models import User, UserActivity
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_view(request):
    """Single view for all charts"""
    context = get_dashboard_data()
    return render(request, 'dashboard/dashboard.html', context)



def get_dashboard_data():
    """Helper function to get all dashboard data"""
    # Date range for timeline data
    end_date = timezone.now()  # Use timezone-aware datetime
    start_date = end_date - timedelta(days=30)
    
    # User Activity Data
    user_activity = (UserActivity.objects
        .filter(last_activity__range=(start_date, end_date))
        .annotate(date=TruncDate('last_activity'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date'))
    
    # Content Distribution Data
    content_distribution = (Content.objects
        .values('content_type')
        .annotate(count=Count('id')))
    
    # Legacy Timeline Data
    legacy_timeline = (FamilyLegacy.objects
        .filter(created_at__range=(start_date, end_date))
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date'))
    
    # Storage Usage Data
    users = User.objects.all()[:10]
    
    return {
        'user_activity': {
            'labels': [activity['date'].strftime('%Y-%m-%d') for activity in user_activity],
            'data': [activity['count'] for activity in user_activity]
        },
        'content_distribution': {
            'labels': [item['content_type'] for item in content_distribution],
            'data': [item['count'] for item in content_distribution]
        },
        'legacy_timeline': {
            'labels': [item['date'].strftime('%Y-%m-%d') for item in legacy_timeline],
            'data': [item['count'] for item in legacy_timeline]
        },
        'storage_usage': {
            'labels': [f"User {user.id}" for user in users],
            'usage': [user.storage_used / (1024 * 1024 * 1024) for user in users],
            'limits': [user.storage_limit / (1024 * 1024 * 1024) for user in users]
        }
    }