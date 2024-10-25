from django.test import TestCase
from apps.content.models import Content
from apps.accounts.models import User

class ContentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_create_content(self):
        content = Content.objects.create(user=self.user, title='Test Content', content_type='document')
        self.assertEqual(content.title, 'Test Content')
        self.assertEqual(content.user, self.user)
