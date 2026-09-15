# Custom authentication and profile management forms
from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for authenticated users to edit first name, last name, and profile photo.
    """
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'profile']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'profile': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }


class CustomLoginForm(AuthenticationForm):
    """
    Customized login form with user-friendly error messaging.
    """
    error_messages = {
        'invalid_login': "The username or password is incorrect. Please try again."
    }


user = get_user_model()


class CustomRegisterForm(UserCreationForm):
    """
    Customized user registration form with optional email support and custom placeholder styling.
    """
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
        # Override error messages and apply custom attributes to username input
        super().__init__(*args, **kwargs)

        self.error_messages['password_mismatch'] = "The two password fields didn't match. Please try again."

        self.fields['username'].widget.attrs.update({
            'style': 'text-transform: none !important;',
            'placeholder': 'Username'
        })