# apps/content/forms.py

from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'content_type', 'file']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),
            'content_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('file'):
            instance.size = self.cleaned_data['file'].size
        if commit:
            instance.save()
        return instance


class ShareContentForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    can_edit = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Allow editing'
    )
    can_delete = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Allow deletion'
    )