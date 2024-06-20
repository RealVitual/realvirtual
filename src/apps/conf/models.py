import os
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from src.contrib.db.models import SingletonModel, BaseModel
from django.contrib.postgres.fields import ArrayField
from django.conf import settings


def get_upload_path(internal_folder):
    return os.path.join(
      "%s/%s/" % (settings.BUCKET_FOLDER_NAME, internal_folder))


class CompanySettings(SingletonModel):
    company_name = models.CharField(
        _('Nombre Cliente'), max_length=255, blank=True)
    logo = models.ImageField(
            _('Logo'), upload_to=get_upload_path('settings'), null=True, blank=True)
    email = models.CharField(
        _('Email de contacto'), max_length=255, blank=True)
    phone = models.CharField(_('teléfono'), max_length=255, blank=True)
    ruc = models.CharField(_('RUC'), max_length=255, blank=True)
    fiscal_address = models.CharField(
        _('dirección fiscal'), max_length=255, blank=True)
    domain = models.URLField(
        _('URL del dominio'), max_length=255, null=True, blank=True)
    contact_email = models.CharField(
        _('email para contacto'), max_length=255, blank=True)
    info_email = models.CharField(
        _('email Info'), max_length=255, blank=True)
    info_phone = models.CharField(
        _('Telefono Info'), max_length=255, blank=True)
    info_facebook = models.CharField(
        _('Facebook Info'), max_length=255, blank=True)
    info_instagram = models.CharField(
        _('Instagram Info'), max_length=255, blank=True)
    info_twitter = models.CharField(
        _('Twitter Info'), max_length=255, blank=True)
    info_pinterest = models.CharField(
        _('Pinterest Info'), max_length=255, blank=True)
    extra_settings = JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = _('Company Settings')
        verbose_name_plural = _('Company Settings')

    def __str__(self):
        return 'Datos del cliente'


class DocumentType(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    code = models.CharField(_('code'), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Tipo de documento")
        verbose_name_plural = _("Tipos de documento")

    def __str__(self):
        return self.name


class CompanyPosition(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    code = models.CharField(_('code'), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Cargo")
        verbose_name_plural = _("Cargos")

    def __str__(self):
        return self.name


class AgeRange(BaseModel):
    position = models.PositiveIntegerField(
        _('Posición'),
        default=0)
    name = models.CharField(_('name'), max_length=255)
    code = models.CharField(_('code'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Rango de edad")
        verbose_name_plural = _("Rangos de edad")
        ordering = ['position']

    def __str__(self):
        return self.name


class Profile(BaseModel):
    code = models.CharField(
        _('code'), max_length=255, blank=True)
    name = models.CharField(
        _('name'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.name


class Country(BaseModel):
    position = models.PositiveIntegerField(
        _('Posición'),
        default=0)
    name = models.CharField(_('name'), max_length=255)
    code = models.CharField(_('code'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("País")
        verbose_name_plural = _("Paises")
        ordering = ['position']

    def __str__(self):
        return self.name


class LandingForm(BaseModel):
    fields = ArrayField(
        base_field=models.CharField(max_length=200),
        blank=True,
        verbose_name=_('fields'),
        null=True
    )
    names = models.BooleanField(
        _('Nombres'), default=True)
    phone = models.BooleanField(
        _('Número de telefono'), default=False)
    address = models.BooleanField(
        _('Dirección'), default=False)
    gender = models.BooleanField(
        _('Género'), default=False)
    document_type = models.BooleanField(
        _('Tipo de documento'), default=False)
    document = models.BooleanField(
        _('N de documento'), default=False)
    date_birth = models.BooleanField(
        _('Fecha de Nacimiento'), default=False)
    occupation = models.BooleanField(
        _('Cargo ocupacional'), default=False
    )
    age_range = models.BooleanField(
        _('Rango de edad'), default=False
    )
    profile_image = models.BooleanField(
        _('Foto de perfil'), default=False
    )
    country = models.BooleanField(
        _('Pais'), default=False
    )

    class Meta:
        verbose_name = _('Formulario Registro')
        verbose_name_plural = _('Formulario Registro')
        ordering = ['-modified']

    def __str__(self):
        return 'Formulario Registro'


class Speciality(BaseModel):
    position = models.PositiveIntegerField(
        _('Posición'),
        default=0)
    name = models.CharField(
        _('name'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Speciality')
        verbose_name_plural = _('Specialities')

    def __str__(self):
        return self.name
