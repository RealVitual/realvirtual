from django import forms
from src.apps.customers.models import Customer
from django.contrib.auth import authenticate
from .models import CustomerInvitedLanding, CredentialCustomer
from .utils import decode_base64_file, generate_credential
from uuid import uuid4
from src.apps.users.models import User
from src.apps.companies.models import UserCompany
from src.apps.companies.models import EmailTemplate, EmailSettings
from django.template import Context, Template
import threading
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from .constants import forms_dict
from src.apps.landing.utils import generate_certificate_pdf


def send_html_mail(subject, html_content, e_mail, receptors,
                   customer, company):
    EmailThread(
        subject, html_content, e_mail, receptors,
        customer, company).start()


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content,
                 e_mail, receptors, customer, company):
        self.subject = subject
        self.e_mail = e_mail
        self.html_content = html_content
        self.receptors = receptors
        self.customer = customer
        self.company = company
        threading.Thread.__init__(self)

    def run(self):
        rules_email, created = EmailSettings.objects.get_or_create(
            company=self.company)
        connection = get_connection(
            host=rules_email.host,
            port=rules_email.port,
            username=rules_email.username,
            password=rules_email.password,
            use_tls=rules_email.use_tls
        )
        # connection.open()
        msg = EmailMessage(
            subject=self.subject,
            body=self.html_content,
            from_email=rules_email.username,
            to=self.receptors,
            connection=connection)
        msg.content_subtype = "html"
        msg.send()
        # connection.close()
        print('SE ENVIÓ CORREO EXITOSAMENTE PARA ==>' + self.receptors[0])


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True)
    can_confirm = forms.CharField(required=False)
    message = forms.CharField(required=False)

    class Meta:
        model = UserCompany
        # fields = ('names', 'email', 'last_name', 'password', 'country',
        #           'occupation', 'job_company', 'company_position',
        #           'confirm_password')
        fields = ('email', 'password', 'confirm_password')
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        self.domain = kwargs["initial"].get("domain")
        self.company = kwargs["initial"].get("company")
        self.access_type = kwargs["initial"].get("access_type", None)
        self.is_confirmartion = kwargs["initial"].get('is_confirmation', False)
        self.in_person = None
        self.virtual = None
        super(RegisterForm, self).__init__(*args, **kwargs)
        fields = self.company.get_form_fields_list()
        for field in fields:
            self.fields[field] = UserCompany._meta.get_field(field).formfield()

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        allow_register, message, can_confirm = self.allow_register(data)
        if not allow_register and not self.is_confirmartion:
            raise forms.ValidationError(dict(message=message,
                                             can_confirm=can_confirm))
        if (can_confirm and self.is_confirmartion) or allow_register:
            try:
                UserCompany.objects.get(email=email.lower(),
                                        company=self.company)
                message = "Ya existe una cuenta con el email ingresado."
                raise forms.ValidationError(dict(message=message,
                                                 can_confirm=False))
            except UserCompany.DoesNotExist:
                print('UserCompany does not exist')
                pass
        return data

    def save(self):
        data = self.cleaned_data
        data.pop('confirm_email', None)
        data.pop('confirm_password', None)
        data.pop('can_confirm', None)
        data.pop('message', None)
        data['in_person'] = self.in_person
        data['virtual'] = self.virtual
        data['email'] = data['email'].lower()
        job_company_select = data.pop('job_company_select', None)
        occupation_select = data.pop('occupation_select', None)
        password = data.pop('password', None)
        customers = Customer.objects.filter(email=data.get('email').lower())
        if customers:
            customer = customers.last()
        else:
            customer = Customer.objects.create(**data)
        customer.set_password(password)
        customer.save()
        confirmed = True
        if self.company.confirm_user:
            confirmed = False
        data['confirmed'] = confirmed
        data['user'] = User.objects.get(email=customer.email)
        data['company'] = self.company
        data['job_company_select'] = job_company_select
        data['occupation_select'] = occupation_select
        user_company = UserCompany.objects.create(
            **data
        )
        user_company.set_password(password)
        user_company.save()

        # Send Email
        mailing, created = EmailTemplate.objects.get_or_create(
            company=self.company, email_type="REGISTER")
        if mailing.from_email:
            context = dict()
            context["names"] = customer.names
            context["first_name"] = customer.names.split(" ")[0]
            context["email"] = customer.email
            context["company"] = self.company

            template = Template(mailing.html_code)
            html_content = template.render(Context(context))
            subject = mailing.subject
            e_mail = u'{0}<{1}>'.format(
                mailing.from_name, mailing.from_email)
            msg = EmailMessage(
                subject, html_content, e_mail, [customer.email, ])
            msg.content_subtype = "html"
            print("ENVIAR CORREO ")
            send_html_mail(
                subject, html_content, e_mail, [customer.email, ],
                customer, self.company)

        user = authenticate(username=customer.email,
                            password=password)
        return dict(user=user, message="", user_company=user_company)

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
        elif access_type in [
                "HYBRID", "IN_PERSON"] and (not self.access_type or self.access_type == "in_person"):
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
        elif self.access_type == "virtual":
            self.in_person = False
            self.virtual = True
            return True, message, False
        else:
            message = ""
            self.in_person = False
            self.virtual = True
            return True, message, False


class CredentialCustomerForm(forms.ModelForm):
    profile_image = forms.CharField(required=False)

    class Meta:
        model = CredentialCustomer
        fields = ('names', 'profile_image')

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
        generate_credential(instance, self.company, full_credential_name)

        return dict(credential=instance, message="Success")


class LoginForm(forms.Form):
    message = forms.CharField(required=False)
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
            user = UserCompany.objects.get(
                email=email.lower(), company=self.company)
        except UserCompany.DoesNotExist:
            message = "Error de Credenciales"
            raise forms.ValidationError(dict(message=message))
        if not user.check_password(password):
            message = "Error de Credenciales"
            raise forms.ValidationError(dict(message=message))
        return data

    def save(self):
        data = self.cleaned_data
        password = data.get("password")
        email = data.get("email")
        credentials = dict(email=email.lower(), password=password)
        user = User.objects.get(email=email.lower())
        # # Authenticate and return user
        # user = authenticate(username=email,
        #                     password=password)
        user_access = data.get('user_access', True)
        message = data.get('message', None)
        return dict(
            user=user, user_access=user_access, message=message,
            credentials=credentials)


class EmailPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())

    def __init__(self, *args, **kwargs):
        self.domain = kwargs['initial'].get('domain')
        self.company = kwargs['initial'].get('company')
        super(EmailPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = "E-mail"

    def clean(self):
        data = self.cleaned_data
        email = data.get("email")
        if not User.objects.filter(email=email.lower()):
            mensaje = "Error de Credenciales"
            raise forms.ValidationError(mensaje)
        return data

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        uuid_hash = str(uuid4())
        user_company = UserCompany.objects.get(
            email=email.lower(), company=self.company)
        user_company.uuid_hash = uuid_hash
        user_company.save()
        url = "%s/reset-password/%s" % (self.domain, uuid_hash)

        # Send Email
        mailing = EmailTemplate.objects.get(company=self.company,
                                            email_type="PASSWORD")
        if mailing.from_email:
            context = dict()
            context["names"] = user_company.names
            context["first_name"] = user_company.names.split(" ")[0]
            context["email"] = user_company.email.lower()
            context["company"] = self.company
            context["url"] = url

            template = Template(mailing.html_code)
            html_content = template.render(Context(context))
            subject = mailing.subject
            e_mail = u'{0}<{1}>'.format(
                mailing.from_name, mailing.from_email)
            msg = EmailMessage(
                subject, html_content, e_mail, [user_company.email, ])
            msg.content_subtype = "html"
            send_html_mail(
                subject, html_content, e_mail, [user_company.email, ],
                user_company, self.company)


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs['initial'].get('user')
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        new_password = data['new_password1']
        new_password_2 = data['new_password2']
        if not new_password == new_password_2:
            mensaje = "Las contraseñas no coinciden"
            raise forms.ValidationError(mensaje)
        return data

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.uuid_hash = ""
        self.user.save()
        return self.user


class CertificateForm(forms.Form):
    full_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs['initial'].get('user')
        self.company_id = kwargs['initial'].get('company_id')
        super(CertificateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        full_name = self.cleaned_data["full_name"]
        user_company = UserCompany.objects.get(
            user__email=self.user, company_id=self.company_id)
        generate_certificate_pdf(user_company, full_name)
        return self.user

