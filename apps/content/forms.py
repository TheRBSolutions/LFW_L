# apps/content/forms.py

from django import forms
from filer.models import Folder  
from .models import Content 

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent']  # 'parent' field is already defined in Filer's Folder model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter folders accessible by the user, if needed
        self.fields['parent'].queryset = Folder.objects.filter(owner=user)  # 'owner' field usage depends on your Filer configuration

class ContentUploadForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'content_type',"file",'folder']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'folder': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(owner=user)




class ShareContentForm(forms.Form):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    can_edit = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Allow editing'
    )
    can_delete = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Allow deletion'
    )
