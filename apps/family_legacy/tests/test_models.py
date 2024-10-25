from django.test import TestCase
from apps.family_legacy.models import FamilyLegacy
from apps.accounts.models import User

class FamilyLegacyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_create_legacy(self):
        legacy = FamilyLegacy.objects.create(user=self.user, title='Legacy Title', content='Legacy Content')
        self.assertEqual(legacy.title, 'Legacy Title')
        self.assertEqual(legacy.user, self.user)
