from django import forms
from django.contrib.auth import authenticate
from src.apps.customers.models import Customer
from src.apps.users.models import User


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        email = data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            mensaje = "No existe una cuenta registrada con ese email"
            raise forms.ValidationError(mensaje)
        if not user.check_password(password):
            mensaje = "El email y password no coinciden"
            raise forms.ValidationError(mensaje)
        return data

    def save(self):
        data = self.cleaned_data
        password = data.get("password")
        email = data.get("email")
        # Authenticate and return user
        user = authenticate(username=email,
                            password=password)
        return user
