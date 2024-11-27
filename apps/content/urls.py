# apps/content/urls.py

from django.urls import path
from . import views



urlpatterns = [
    # Main content views
    path('', views.content_list, name='content_list'),
    path('my/', views.views_my_content, name='my_content'),
    path('upload/', views.upload_content, name='upload_content'),
    
    # Content actions
    path('<int:pk>/', views.views_view_content, name='view_content'),
    path('<int:pk>/delete/', views.delete_content, name='delete_content'),
    path('<int:pk>/share/', views.share_content, name='share_content'),
    path('admin/upload_content/<int:folder_id>/', upload_content, name='admin_upload_content'),
    path('admin/folder/<int:folder_id>/', folder_detail, name='admin_folder_detail'),
]