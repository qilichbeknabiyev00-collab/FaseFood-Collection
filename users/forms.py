from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email manzil")

    User = get_user_model()

    class Meta:
        model = User
        fields = ['username', 'email','password']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'role', 'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'role': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'groups': forms.SelectMultiple(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'style': 'height: 120px;'
            }),
            'user_permissions': forms.SelectMultiple(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'style': 'height: 250px;'
            }),
        }