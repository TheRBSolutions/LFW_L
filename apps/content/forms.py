from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'content_type', 'file', 'exclude_from_legacy']
        # size is handled automatically, so we don't include it in fields

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Set the file size if a file was uploaded
        if self.cleaned_data.get('file'):
            instance.size = self.cleaned_data['file'].size
        if commit:
            instance.save()
        return instance