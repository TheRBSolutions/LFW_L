from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from apps.content.forms import ContentUploadForm

class ContentUploadFormTest(TestCase):
    def test_valid_file_size(self):
        valid_file = SimpleUploadedFile('file.mp4', b'file_content', content_type='video/mp4')
        form = ContentUploadForm(data={'title': 'Test Content'}, files={'file': valid_file})
        self.assertTrue(form.is_valid())

    def test_exceeding_file_size(self):
        large_file = SimpleUploadedFile('file.mp4', b'file_content' * 1000000, content_type='video/mp4')
        form = ContentUploadForm(data={'title': 'Test Content'}, files={'file': large_file})
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)
