# Forms for handling article inputs with custom Bootstrap widgets
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    """
    ModelForm for Article model with custom UI widget styling.
    """
    class Meta:
        model = Article
        fields = ['title', 'body', 'cover', 'category', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type article title...',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your article content here...',
                'rows': 8,
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
        }