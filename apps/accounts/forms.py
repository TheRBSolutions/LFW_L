from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    country = forms.CharField(required=False)
    profession = forms.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 
                 'date_of_birth', 'country', 'profession')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'registrationForm'
        self.helper.form_method = 'post'
        self.helper.form_novalidate = True
        
        # Define the layout
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='mb-4'),
                Column('last_name', css_class='mb-4'),
                Column('email', css_class='mb-4'),
                css_class='grid grid-cols-1 gap-4 md:grid-cols-3'
            ),
            Row(
                Column('password1', css_class='mb-4'),
                Column('password2', css_class='mb-4'),
                Column('date_of_birth', css_class='mb-4'),
                css_class='grid grid-cols-1 gap-4 md:grid-cols-3'
            ),
            Row(
                Column('country', css_class='mb-4'),
                Column('profession', css_class='mb-4'),
                css_class='grid grid-cols-1 gap-4 md:grid-cols-2'
            ),
            Row(
                Column(
                    Submit('submit', 'Register', css_class='w-full px-4 py-2 text-white transition bg-blue-500 rounded hover:bg-blue-600'),
                    css_class='mt-4'
                )
            ),
            HTML('<p class="mt-4 text-center"><a href="{% url "login" %}" class="text-blue-500 hover:underline">Already have an account? Login</a></p>')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Automatically make the user a staff member
        if commit:
            user.save()
        return user
