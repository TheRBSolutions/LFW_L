from django.test import TestCase
from apps.accounts.forms import SignupForm

class SignupFormTest(TestCase):
    def test_password_matching(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'date_of_birth': '1990-01-01'
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password456'
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)
