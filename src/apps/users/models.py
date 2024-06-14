from uuid import uuid4
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    Group, Permission, BaseUserManager, AbstractBaseUser, PermissionsMixin,
)
from model_utils.models import TimeStampedModel
from django.conf import settings
from src.contrib.db.models import BaseModel
from src.apps.conf.models import DocumentType, AgeRange, Country
from src.apps.companies.models import Company


class UserManager(BaseUserManager):
    def _create_user(self, email, password, schema_name=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,
                    email=None,
                    password=None,
                    schema_name=None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, schema_name, **extra_fields)

    def create_superuser(self,
                         email,
                         password,
                         schema_name=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, schema_name, **extra_fields)


class TesterManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_tester=True)

    def _create_user(self, email, password, schema_name=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,
                    email=None,
                    password=None,
                    schema_name=None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_tester', True)
        return self._create_user(email, password, schema_name, **extra_fields)

    def create_superuser(self,
                         email,
                         password,
                         schema_name=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_tester', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Tester Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Tester Superuser must have is_superuser=True.')
        if extra_fields.get('is_tester') is not True:
            raise ValueError('Tester Superuser must have is_tester=True.')

        return self._create_user(email, password, schema_name, **extra_fields)


class User(BaseModel, PermissionsMixin, AbstractBaseUser):
    """
    Extends standard Django User
    """
    MALE = 'male'
    FEMALE = 'female'
    SR = 'mr'
    SRA = 'ms'

    GENDER_CHOICES = ((MALE, _("Hombre")), (FEMALE, _('Mujer')))
    PREFIX = ((SR, _("Sr.")), (SRA, _("Sra.")))
    prefix = models.CharField(
        "Prefijo", choices=PREFIX, null=True, blank=True, max_length=120)
    names = models.CharField(
        _('Names'), null=True, max_length=100, blank=True)
    first_name = models.CharField(
        _('First name'), null=True, max_length=100, blank=True)
    last_name = models.CharField(
        _('Last name'), null=True, max_length=100, blank=True)
    first_surname = models.CharField(
        _('First surname'), max_length=100, null=True, blank=True)
    last_surname = models.CharField(
        _('Last surname'), max_length=100, null=True, blank=True)
    full_name = models.CharField(
        _('Full name'), null=True, max_length=100, blank=True)
    email = models.EmailField(
        _('Email address'), unique=True, null=True,
        error_messages={'unique': "El email ya se encuentra registrado."})
    has_email_confirmed = models.BooleanField(
        _('email confirmed?'),
        default=False,
        help_text=_('Designates whether this user should be '
                    'treated as email confirmed.'
                    ' Unselect this instead of uncofirmed email.'))
    uuid_hash = models.CharField(
        'UUID',
        max_length=36,
        default='',
        blank=True,
        help_text=_('Random UUID hash to remember password.'))
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can ' +
                    'log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'),
    )
    is_tester = models.BooleanField(
        _('tester account'),
        default=False,
        help_text=_('Designates whether this user should be treated as '
                    'tester account. '
                    'Select this when need test experience.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone = models.CharField(_('phone'), max_length=50, null=True, blank=True)
    mobile = models.CharField(
        _('mobile'), max_length=50, null=True, blank=True)
    gender = models.CharField(
        _('gender'),
        choices=GENDER_CHOICES,
        max_length=30,
        null=True,
        blank=True)
    document_type = models.ForeignKey(
        DocumentType, related_name="%(class)s_set",
        on_delete=models.CASCADE, null=True, blank=True)
    document = models.CharField(
        _("document"), max_length=120, null=True, blank=True)
    date_birth = models.DateField(_('date birth'), null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="%(class)s_set",
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'),
        related_query_name="%(class)s",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="%(class)s_set",
        help_text=_('Specific permissions for this user.'),
        related_query_name="%(class)s",
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    facebook_id = models.CharField(max_length=255, null=True, blank=True)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(
        'Profesion ', max_length=255, blank=True, null=True)
    jon_company = models.CharField(
        'Empresa / II.EE.', max_length=255, blank=True, null=True)
    company_position = models.CharField(
        'Cargo / Carrera', max_length=255, blank=True, null=True)
    speciality = models.ForeignKey(
        'conf.Speciality', related_name="specialities_users",
        on_delete=models.DO_NOTHING, null=True, blank=True)
    age_range = models.ForeignKey(
        AgeRange, related_name="age_range_users",
        on_delete=models.CASCADE, null=True, blank=True)
    is_worker = models.BooleanField('Colaborador', default=False)
    objects = UserManager()
    profile_image = models.ImageField(
        _('Imagen Perfil'), upload_to='profile_img', null=True, blank=True)
    credential_img = models.ImageField(
        _('credential'), upload_to='credentials', null=True, blank=True)
    being_used = models.BooleanField(_("Siendo usado"), default=False)
    address = models.CharField(
        _("direccion"), max_length=255, null=True, blank=True)
    has_shared = models.BooleanField(
        verbose_name=_('Ha compartido'), default=False
    )
    generated_credential = models.BooleanField(
            verbose_name=_('Ha generado credencial'), default=False
        )
    country = models.ForeignKey(
        Country, related_name="country_users",
        on_delete=models.DO_NOTHING, null=True, blank=True)
    received_welcome_email = models.BooleanField(
        _("Recibió correo"), default=False)
    avoid_credential = models.BooleanField(
        _("Avoid credential"), default=False)
    certificate = models.FileField(
        _('certificado'), upload_to="certificates",
        null=True, blank=True)
    virtual = models.BooleanField(_('Virtual'), default=False)
    in_person = models.BooleanField(_('In Person'), default=False)
    company = models.ForeignKey(Company, related_name="company_users",
                                null=True, blank=True, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):

        if not self.uuid_hash:
            self.uuid_hash = str(uuid4())
        if not self.full_name:
            self.full_name = f'{self.names} {self.last_name}'

        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = [self.first_name, self.first_surname, self.last_surname]
        full_name = [name for name in full_name if name and str(name).strip()]
        full_name = ' '.join(full_name)

        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def name_only(self):
        name = self.names.split(' ')
        if len(name) > 1:
            return name[0]
        return name

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-modified']

    def __string__(self):
        return '{} | {}'.format(self.email, self.get_full_name())


class Administrator(User):
    class Meta:
        verbose_name = _('Administrator')
        verbose_name_plural = _('Administrators')
        ordering = ['-modified']


class UserSession(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')
        ordering = ['-created']

    def __string__(self):
        return '{}'.format(self.user.email)
