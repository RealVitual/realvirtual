from django import forms
from django.contrib.auth import authenticate
from src.apps.customers.models import Customer
from src.apps.companies.models import UserCompany
from src.apps.users.models import User


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.company = kwargs["initial"].get("company")
        self.user = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        email = data.get("email")
        try:
            user = UserCompany.objects.get(
                email=email, company=self.company, is_admin=True)
            self.user = user.user
        except User.DoesNotExist:
            mensaje = "Error de credenciales"
            raise forms.ValidationError(mensaje)
        if not user.check_password(password):
            mensaje = "Error de credenciales"
            raise forms.ValidationError(mensaje)
        return data

    def save(self):
        data = self.cleaned_data
        return self.user
