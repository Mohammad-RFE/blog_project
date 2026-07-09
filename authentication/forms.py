from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'profile']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'profile': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }


class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "The username or password is incorrect. Please try again."
    }


user = get_user_model()


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email (Optional)',
        'style': 'text-transform: none !important;'
    }))

    class Meta:
        model = user
        fields = ['username', 'email']

        error_messages = {
            'username': {
                'unique': "This username is already taken. Please choose another one.",
            },
            'email': {
                'unique': "This email is already registered.",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_messages['password_mismatch'] = "The two password fields didn't match. Please try again."

        self.fields['username'].widget.attrs.update({
            'style': 'text-transform: none !important;',
            'placeholder': 'Username'
        })