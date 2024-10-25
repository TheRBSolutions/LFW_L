from django.test import TestCase
from apps.family_legacy.forms import FamilyLegacyForm

class FamilyLegacyFormTest(TestCase):
    def test_valid_content(self):
        form_data = {'title': 'Legacy Title', 'description': 'Some description', 'content': 'This is legacy content.'}
        form = FamilyLegacyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_content(self):
        form_data = {'title': 'Legacy Title', 'description': 'Some description', 'content': ''}
        form = FamilyLegacyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
