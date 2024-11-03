from ninja import Schema

# Schema Definitions for API Responses
class UserMetricsSchema(Schema):
    total_users: int
    active_users: int
    online_users: int
    new_users_today: int
    total_storage_used: int
    average_storage_used: float

class ContentMetricsSchema(Schema):
    total_content: int
    content_by_type: dict
    total_storage: int
    excluded_from_legacy: int

class LegacyMetricsSchema(Schema):
    total_legacies: int
    active_legacies: int
    average_content_per_legacy: float

class TimeSeriesDataSchema(Schema):
    labels: list
    data: list

class DashboardResponseSchema(Schema):
    user_metrics: UserMetricsSchema
    content_metrics: ContentMetricsSchema
    legacy_metrics: LegacyMetricsSchema
    user_growth: TimeSeriesDataSchema
    content_distribution: dict
    hourly_activity: TimeSeriesDataSchema
    storage_usage: TimeSeriesDataSchema
    recent_activities: list
