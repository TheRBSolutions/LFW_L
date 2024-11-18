# core/api.py
from ninja import NinjaAPI

# Create a single API instance
api = NinjaAPI()

# We'll register routers here instead of in urls.py
def setup_api_routes():
    from apps.dashboard.api import router as dashboard_router
    api.add_router("/dashboard", dashboard_router)

# Initialize routes
setup_api_routes()
