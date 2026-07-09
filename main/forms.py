from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'email', 'body']

        widgets = {
    'subject': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject',
        'style': 'text-transform: none !important;'
    }),
    'email': forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email Address',
        'style': 'text-transform: none !important;'
    }),
    'body': forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your message here...',
        'rows': 6,
        'style': 'text-transform: none !important;'
    }),
}