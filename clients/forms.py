from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ф.И.О.'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий'}),
        }
