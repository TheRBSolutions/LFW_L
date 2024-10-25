from django import forms
from .models import FamilyLegacy

class FamilyLegacyForm(forms.ModelForm):
    class Meta:
        model = FamilyLegacy
        fields = ['title', 'description', 'content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Content cannot be empty.")
        return content
