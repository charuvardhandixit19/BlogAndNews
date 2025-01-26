# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise ValidationError("User with this username does not exist.")
        return username
