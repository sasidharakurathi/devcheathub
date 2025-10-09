from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'off'}),
            'first_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'github_url', 'linkedin_url']
        widgets = {
            'bio': forms.TextInput(attrs={'autocomplete': 'off'}),
            'profile_picture': forms.EmailInput(attrs={'autocomplete': 'off'}),
            'github_url': forms.TextInput(attrs={'autocomplete': 'off'}),
            'linkedin_url': forms.TextInput(attrs={'autocomplete': 'off'}),
        }