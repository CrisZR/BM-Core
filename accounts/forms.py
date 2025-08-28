from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese el usuario", "autofocus": True}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Ingrese la contraseña"}),
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Recuerdame")
    
    def clean(self):
        cleaned = super().clean()
        login_input = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        return cleaned