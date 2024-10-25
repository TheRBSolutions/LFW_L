from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.content.models import Content

User = get_user_model()

class ContentViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.content = Content.objects.create(user=self.user, title='Test Content', content_type='document')

    def test_content_list_view(self):
        response = self.client.get(reverse('content:content_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/content_list.html')

    def test_upload_content_view(self):
        response = self.client.get(reverse('content:upload_content'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/upload_content.html')

        post_data = {
            'title': 'New Content',
            'content_type': 'document',
        }
        file_data = {'file': Content.objects.create(user=self.user, title='New Content').file}
        response = self.client.post(reverse('content:upload_content'), data=post_data)
        self.assertEqual(response.status_code, 200)
