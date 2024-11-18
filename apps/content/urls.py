# apps/content/urls.py

from django.urls import path
from .views import (
    views_my_content,
    content_list,
    upload_content,
    delete_content,
    share_content,
    views_view_content
)



urlpatterns = [
    # Main content views
    path('', content_list, name='content_list'),
    path('my/', views_my_content, name='my_content'),
    path('upload/', upload_content, name='upload_content'),
    
    # Content actions
    path('<int:pk>/', views_view_content, name='view_content'),
    path('<int:pk>/delete/', delete_content, name='delete_content'),
    path('<int:pk>/share/', share_content, name='share_content'),
]