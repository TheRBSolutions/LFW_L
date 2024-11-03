from ninja import Router
from typing import Dict, Any

# Import the DashboardMetricsService
from .services.dashboard_service import DashboardMetricsService

router = Router()

@router.get("/data")
def get_dashboard_data(request) -> Dict[str, Any]:
    """API endpoint for dashboard data"""
    try:
        # Initialize the service
        service = DashboardMetricsService()

        # Fetch data using the service methods
        user_metrics = service.get_user_metrics()
        content_metrics = service.get_content_metrics()
        legacy_metrics = service.get_legacy_metrics()
        user_growth = service.get_user_growth()
        content_distribution = service.get_content_distribution()
        hourly_activity = service.get_hourly_activity()
        storage_usage_trend = service.get_storage_usage_trend()
        recent_activities = service.get_recent_activities()

        # Prepare the response data
        return {
            'user_metrics': user_metrics,
            'content_metrics': content_metrics,
            'legacy_metrics': legacy_metrics,
            'user_growth': user_growth,
            'content_distribution': content_distribution,
            'hourly_activity': hourly_activity,
            'storage_usage_trend': storage_usage_trend,
            'recent_activities': recent_activities,
        }
    except Exception as e:
        print(f"Error in get_dashboard_data: {str(e)}")
        return {}
