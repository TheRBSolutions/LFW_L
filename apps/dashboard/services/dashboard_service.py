# apps/dashboard/services/dashboard_service.py
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncDate, ExtractHour

from apps.accounts.models import User, UserActivity
from apps.content.models import Content
from apps.family_legacy.models import FamilyLegacy

class DashboardMetricsService:
    def __init__(self):
        self.now = timezone.now()
        self.today_start = self.now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.thirty_days_ago = self.now - timedelta(days=30)

    def get_user_metrics(self):
        online_threshold = self.now - timedelta(minutes=5)
        total_users = User.objects.count()
        active_users = UserActivity.objects.filter(last_activity__gte=self.thirty_days_ago).values('user').distinct().count()
        online_users = UserActivity.objects.filter(last_activity__gte=online_threshold).values('user').distinct().count()
        new_users_today = User.objects.filter(date_joined__gte=self.today_start).count()
        total_storage_used = User.objects.aggregate(total=Sum('storage_used'))['total'] or 0
        average_storage_used = User.objects.filter(storage_used__gt=0).aggregate(
            avg=Sum('storage_used') / Count('id')
        )['avg'] or 0
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "online_users": online_users,
            "new_users_today": new_users_today,
            "total_storage_used": total_storage_used,
            "average_storage_used": average_storage_used
        }

    def get_content_metrics(self):
        total_content = Content.objects.count()
        content_by_type = dict(
            Content.objects.values('content_type')
            .annotate(count=Count('id'))
            .values_list('content_type', 'count')
        )
        total_storage = Content.objects.aggregate(total=Sum('size'))['total'] or 0
        excluded_from_legacy = Content.objects.filter(exclude_from_legacy=True).count()
        
        return {
            "total_content": total_content,
            "content_by_type": content_by_type,
            "total_storage": total_storage,
            "excluded_from_legacy": excluded_from_legacy
        }

    def get_legacy_metrics(self):
        total_legacies = FamilyLegacy.objects.count()
        active_legacies = FamilyLegacy.objects.filter(content__isnull=False).distinct().count()
        average_content_per_legacy = (
            Content.objects.filter(exclude_from_legacy=False).count() / total_legacies
            if total_legacies > 0 else 0
        )
        
        return {
            "total_legacies": total_legacies,
            "active_legacies": active_legacies,
            "average_content_per_legacy": average_content_per_legacy
        }

    def get_user_growth(self):
        user_growth = User.objects.filter(date_joined__gte=self.thirty_days_ago).annotate(
            date=TruncDate('date_joined')
        ).values('date').annotate(count=Count('id')).order_by('date')
        
        return {
            "labels": [entry['date'].strftime('%Y-%m-%d') for entry in user_growth],
            "data": [entry['count'] for entry in user_growth]
        }

    def get_content_distribution(self):
        content_distribution = dict(
            Content.objects.values('content_type')
            .annotate(count=Count('id'))
            .values_list('content_type', 'count')
        )
        return content_distribution

    def get_hourly_activity(self):
        hourly_activity = UserActivity.objects.filter(last_activity__gte=self.today_start).annotate(
            hour=ExtractHour('last_activity')
        ).values('hour').annotate(count=Count('id')).order_by('hour')
        
        return {
            "labels": [entry['hour'] for entry in hourly_activity],
            "data": [entry['count'] for entry in hourly_activity]
        }

    def get_storage_usage_trend(self):
        storage_usage = Content.objects.filter(created_at__gte=self.thirty_days_ago).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(total_size=Sum('size')).order_by('date')
        
        return {
            "labels": [entry['date'].strftime('%Y-%m-%d') for entry in storage_usage],
            "data": [entry['total_size'] for entry in storage_usage]
        }

    def get_recent_activities(self):
        recent_activities = []

        recent_users = User.objects.order_by('-date_joined')[:5]
        for user in recent_users:
            recent_activities.append({
                "type": "registration",
                "description": f"New user registered: {user.email}",
                "timestamp": user.date_joined.isoformat(),
                "metadata": {
                    "country": user.country,
                    "storage_used": user.storage_used
                }
            })

        recent_content = Content.objects.order_by('-created_at')[:5]
        for content in recent_content:
            recent_activities.append({
                "type": "content_upload",
                "description": f"New {content.content_type} uploaded: {content.title}",
                "timestamp": content.created_at.isoformat(),
                "metadata": {
                    "size": content.size,
                    "type": content.content_type
                }
            })

        recent_legacies = FamilyLegacy.objects.order_by('-created_at')[:5]
        for legacy in recent_legacies:
            recent_activities.append({
                "type": "legacy_creation",
                "description": f"New legacy created: {legacy.title}",
                "timestamp": legacy.created_at.isoformat(),
                "metadata": {
                    "user": legacy.user.email
                }
            })

        recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return recent_activities
