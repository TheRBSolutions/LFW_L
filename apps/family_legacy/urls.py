from django.urls import path
from .views import legacy_list, add_legacy

urlpatterns = [
    path('', legacy_list, name='legacy_list'),
    path('add/', add_legacy, name='add_legacy'),
]
