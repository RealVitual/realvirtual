from django import forms
from src.apps.customers.models import Customer
from django.contrib.auth import authenticate
from .models import CustomerInvitedLanding, CredentialCustomer
from .utils import decode_base64_file, generate_credential


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True)
    can_confirm = forms.CharField(required=False)
    message = forms.CharField(required=False)

    class Meta:
        model = Customer
        fields = ('names', 'email', 'last_name', 'password', 'country',
                  'occupation', 'jon_company', 'company_position',
                  'confirm_password')
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        self.domain = kwargs["initial"].get("domain")
        self.company = kwargs["initial"].get("company")
        self.is_confirmartion = kwargs["initial"].get('is_confirmation', False)
        self.in_person = None
        self.virtual = None
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        data = self.cleaned_data
        email = data.get('email')
        allow_register, message, can_confirm = self.allow_register(data)
        if not allow_register and not self.is_confirmartion:
            raise forms.ValidationError(dict(message=message,
                                             can_confirm=can_confirm))
        if (can_confirm and self.is_confirmartion) or allow_register:
            try:
                Customer.objects.get(email=email, company=self.company)
                mensaje = "Ya existe una cuenta con el email ingresado."
                raise forms.ValidationError(mensaje)
            except Customer.DoesNotExist:
                print('customer does not exist')
                pass
        return data

    def save(self):
        data = self.cleaned_data
        data.pop('confirm_email', None)
        data.pop('confirm_password', None)
        data.pop('can_confirm', None)
        data.pop('message', None)
        print(data, 'DATA')
        data['company'] = self.company
        data['in_person'] = self.in_person
        data['virtual'] = self.virtual
        password = data.pop('password', None)
        customer = Customer.objects.create(**data)
        customer.set_password(password)
        customer.save()
        user = authenticate(username=customer.email,
                            password=password)
        return dict(user=user, message="")

    def allow_register(self, data):
        message = ""
        access_type = self.company.access_type
        if self.company.is_private:
            found_invited_customer = CustomerInvitedLanding.objects.filter(
                company=self.company, email=data.get('email'))
            if found_invited_customer:
                self.in_person = found_invited_customer.in_person
                self.virtual = found_invited_customer.virtual
                return True, message, True
            elif self.company.allow_virtual_access and \
                    access_type == "HYBRID":
                message = "Sólo Podrás acceder al evento de forma virtual. ¿Deseas continuar?"  # noqa
                self.in_person = False
                self.virtual = True
                return True, message, True
            else:
                message = "No estás en la base de datos de invitados"
                return False, message, False
        if access_type in [
                "HYBRID", "IN_PERSON"]:
            if self.company.current_quantity < self.company.capacity:
                self.in_person = True
                self.virtual = False
                return True, message, True
            elif access_type == "IN_PERSON":
                message = "Lo sentimos, el aforo está completo"
                return False, message, False
            else:
                self.in_person = False
                self.virtual = True
                message = "Sólo Podrás acceder al evento de forma virtual. ¿Deseas continuar?" # noqa
                return False, message, True


class CredentialCustomerForm(forms.ModelForm):
    profile_image = forms.CharField(required=False)

    class Meta:
        model = CredentialCustomer
        fields = ('names', )

    def __init__(self, *args, **kwargs):
        self.date_name = kwargs["initial"].get("date_name")
        self.user = kwargs['initial'].get('user')
        self.company = kwargs['initial'].get('company')
        super(CredentialCustomerForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        image_code = data.pop('profile_image')
        data['user'] = self.user
        data['company'] = self.company
        instance = CredentialCustomer.objects.create(**data)
        names = data.get('names').replace(' ', '_')
        full_credential_name = "%s_%s" % (names, self.date_name)
        user = self.user

        if image_code:
            profile_image = decode_base64_file(
                image_code, full_credential_name)
            instance.profile_image = profile_image
            user.profile_image = profile_image
            instance.save()
        else:
            user.profile_image = ""
        user.generated_credential = True
        user.credential_code = instance.code
        user.save()
        generate_credential(instance, full_credential_name)

        return dict(credential=instance, message="Success")


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.company = kwargs["initial"].get("company")
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = "E-mail"
        self.fields['password'].widget.attrs['placeholder'] = "Contraseña"

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        email = data.get("email")
        try:
            user = Customer.objects.get(email=email, company=self.company)
        except Customer.DoesNotExist:
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
        credentials = dict(email=email, password=password)
        # Authenticate and return user
        user = authenticate(username=email,
                            password=password)
        user_access = data.get('user_access', True)
        message = data.get('message', None)
        return dict(
            user=user, user_access=user_access, message=message,
            credentials=credentials)
