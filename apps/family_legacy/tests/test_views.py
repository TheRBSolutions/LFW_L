from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.family_legacy.models import FamilyLegacy

User = get_user_model()

class FamilyLegacyViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.legacy = FamilyLegacy.objects.create(user=self.user, title='Legacy Title', content='Some content')

    def test_legacy_list_view(self):
        response = self.client.get(reverse('family_legacy:legacy_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_legacy/legacy_list.html')

    def test_add_legacy_view(self):
        response = self.client.get(reverse('family_legacy:add_legacy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_legacy/add_legacy.html')

        post_data = {
            'title': 'New Legacy',
            'description': 'New Description',
            'content': 'Legacy Content',
        }
        response = self.client.post(reverse('family_legacy:add_legacy'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family_legacy:legacy_list'))
