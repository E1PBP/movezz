from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full bg-white text-gray-800 placeholder-gray-400 border-gray-300 focus:border-lime-400 focus:ring-2 focus:ring-lime-400/20 transition-all duration-200",
                "placeholder": "Enter your username",
                "autocomplete": "username",
                "required": True,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full bg-white text-gray-800 placeholder-gray-400 border-gray-300 focus:border-lime-400 focus:ring-2 focus:ring-lime-400/20 transition-all duration-200",
                "placeholder": "Password",
                "autocomplete": "current-password",
                "required": True,
            }
        )
    )
    
class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full bg-white text-gray-800 placeholder-gray-400 border-gray-300 focus:border-lime-400 focus:ring-2 focus:ring-lime-400/20 transition-all duration-200",
                "placeholder": "Enter username",
                "autocomplete": "username",
                "required": True,
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full bg-white text-gray-800 placeholder-gray-400 border-gray-300 focus:border-lime-400 focus:ring-2 focus:ring-lime-400/20 transition-all duration-200",
                "placeholder": "Password",
                "autocomplete": "new-password",
                "required": True,
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full bg-white text-gray-800 placeholder-gray-400 border-gray-300 focus:border-lime-400 focus:ring-2 focus:ring-lime-400/20 transition-all duration-200",
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
                "required": True,
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]