from typing import Set
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.forms import fields, widgets
from django.utils.translation import gettext, gettext_lazy as _
from .models import Customer

#"""-------------------------- SignUp Form --------------------------"""
class SignupForm(UserCreationForm):
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

#"""-------------------------- Login Form --------------------------"""
class LoginForm(AuthenticationForm):
    username = UsernameField(
        required=True,
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autofocus": "current-password", "class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "password"]

#""-------------------------- ChangePassword Form --------------------------"""
class MyChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
            }))
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}))

    class Meta:
        model = User
        fields = ["old_password", "new__password1", "new__password2"]

#"""-------------------------- Reset Password Form --------------------------"""
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Enter Registered Email Address "),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": "form-control"}))

#"""-------------------------- Set New Password Form --------------------------"""
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(
        label=_("Confirm New Password "),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}))

#"""-------------------------- Customer Profile Form --------------------------"""
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "locality", "city", "state", "zipcode", "country"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "locality": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "zipcode": forms.NumberInput(attrs={"class": "form-control"}),
            "state": forms.Select(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
        }

