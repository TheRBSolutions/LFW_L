from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'file', 'content_type']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file.size > 10485760:  # 10MB limit
            raise forms.ValidationError("File size exceeds 10MB.")
        return file
