from django.urls import path
from .views import content_list, upload_content, delete_content

urlpatterns = [
    path('', content_list, name='content_list'),
    path('upload/', upload_content, name='content_upload'),
    path('<int:pk>/delete/', delete_content, name='delete_content'),
]
