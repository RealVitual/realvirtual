import os
from django.conf import settings
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from src.contrib.db.models import BaseModel
from src.apps.companies.models import Company
from src.apps.users.models import User


def get_upload_path(internal_folder):
    return os.path.join(
      "%s/%s/" % (settings.BUCKET_FOLDER_NAME, internal_folder))


class Sponsor(BaseModel):
    company = models.ForeignKey(
        Company, related_name="sponsors",
        on_delete=models.CASCADE, null=True)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    name = models.CharField(
        _('Name'), max_length=255, blank=True)
    image = models.ImageField(
        _('Imagen'),
        upload_to=get_upload_path('sponsors'), null=True, blank=True)

    class Meta:
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    def __str__(self):
        return self.name


class Video(BaseModel):
    company = models.ForeignKey(
        Company, related_name="videos",
        on_delete=models.CASCADE, null=True)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    name = models.CharField(
        _('Name'), max_length=255, blank=True)
    image = models.ImageField(
        _('Imagen'),
        upload_to=get_upload_path('videos'), null=True, blank=True)
    description = models.TextField(
        _('Descripcion'), blank=True)
    video_url = models.URLField(
        _('Video URL'), blank=True, null=True)

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __str__(self):
        if self.name:
            return self.name
        return self.description


class ExternalEvent(BaseModel):
    company = models.ForeignKey(
        Company, related_name="external_events",
        on_delete=models.CASCADE, null=True)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    name = models.CharField(
        _('Name'), max_length=255, blank=True)
    event_date = models.CharField(
        _('Event date'), max_length=255, blank=True)
    event_time = models.CharField(
        _('Event time'), max_length=255, blank=True)
    addreess = models.CharField(
        _('Address'), max_length=255, blank=True)
    image = models.ImageField(
        _('Imagen'),
        upload_to=get_upload_path('videos'), null=True, blank=True)
    link = models.CharField(
        _('Link'), max_length=255, blank=True)

    class Meta:
        verbose_name = _("External event")
        verbose_name_plural = _("External events")

    def __str__(self):
        return self.name


class CustomerInvitedLanding(BaseModel):
    company = models.ForeignKey(
        Company, related_name="invited_customers",
        on_delete=models.CASCADE, null=True)
    names = models.CharField(
        _('names'), null=True, max_length=30, blank=True)
    email = models.EmailField(
            _('email address'), null=True)
    first_name = models.CharField(
        _('first name'), null=True, max_length=30, blank=True)
    first_surname = models.CharField(
        _('first surname'), max_length=30, null=True, blank=True)
    last_surname = models.CharField(
        _('last surname'), max_length=30, null=True, blank=True)
    custom_url = models.CharField(
        _('custom url'), max_length=255, blank=True, null=True
    )
    custom_image_url = models.CharField(
        _('custom image url'), max_length=255, blank=True, null=True
    )
    in_person = models.BooleanField(_('Is Present'), default=False)
    virtual = models.BooleanField(_('Is Virtual'), default=False)

    class Meta:
        verbose_name = _('Invitado Landing')
        verbose_name_plural = _('Invitados Landing')
        ordering = ['-modified']

    def __str__(self):
        return self.email


class CredentialCustomer(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_credentials",
        on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User, related_name="credentials", on_delete=models.CASCADE)
    names = models.CharField(
        _('names'), null=True, max_length=100, blank=True)
    profile_image = models.ImageField(
        _('Imagen Perfil'),
        upload_to=get_upload_path('profile_img'),
        null=True, blank=True)
    credential_img = models.ImageField(
        _('credential'),
        upload_to=get_upload_path('credentials'),
        null=True, blank=True)
    code = models.CharField(
        verbose_name=_('Codigo de acceso URL'), max_length=255, null=True)

    class Meta:
        verbose_name = _('Credencial')
        verbose_name_plural = _('Credenciales')
        ordering = ['-modified']

    def __string__(self):
        return self.names

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid4())

        super(CredentialCustomer, self).save(*args, **kwargs)


class CredentialSettings(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_credential_settings",
        on_delete=models.CASCADE, null=True)
    title_credential = models.CharField(
        verbose_name=_('Titulo credencial'),
        max_length=255, null=True, blank=True)
    image_credential = models.ImageField(
        _('Imagen Fondo'),
        upload_to=get_upload_path('credentials_backgrounds'),
        null=True, blank=True)
    default_avatar = models.ImageField(
        _('Default Avatar'),
        upload_to=get_upload_path('avatars'),
        null=True, blank=True)
    first_text_message = models.CharField(
        verbose_name=_('Primer mensaje Exito'),
        max_length=255, null=True, blank=True)
    second_text_message = models.CharField(
        verbose_name=_('Segundo mensaje Exito'),
        max_length=255, null=True, blank=True)

    html_code = models.TextField('Código HTML', blank=True)
    zoom = models.PositiveIntegerField(_('Zoom'), default=1)
    crop_h = models.PositiveIntegerField(_('Crop-h'), default=0)
    crop_w = models.PositiveIntegerField(_('Crop-w'), default=0)
    crop_x = models.PositiveIntegerField(_('Crop-x'), default=0)
    crop_y = models.PositiveIntegerField(_('Crop-y'), default=0)

    class Meta:
        verbose_name = _('Configuración de Credencial')
        verbose_name_plural = _('Configuraciones de Credencial')

    def __str__(self):
        return f"{self.company}"


class Question(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_questions",
        on_delete=models.CASCADE, null=True)
    position = models.SmallIntegerField(_('Posición'), default=1)
    name = models.CharField(_('Nombre'), max_length=255)
    image = models.FileField(
        _('Imagen icon'),
        upload_to=get_upload_path('icons'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('Pregunta')
        verbose_name_plural = _('Preguntas')
        ordering = ['company', 'position']

    def __str__(self):
        return self.name

    def get_choices(self):
        return self.choice_questions.order_by('position')


class ChoiceQuestion(BaseModel):
    question = models.ForeignKey(
        Question,
        related_name='choice_questions',
        on_delete=models.CASCADE)
    position = models.SmallIntegerField(_('Posición'), default=1)
    name = models.CharField(
        _('Nombre'),
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Opción')
        verbose_name_plural = _('Opciones')
        ordering = ['position', '-modified']

    def __str__(self):
        if self.name:
            return self.name
        return self.question.question


class UserAnswer(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_answers",
        on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(
        Question,
        related_name='answer_questions',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    choice_question = models.ForeignKey(
        ChoiceQuestion,
        related_name='answer_choice_questions',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    user = models.ForeignKey(
        User,
        related_name='user_answers',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Respuesta de Usuario')
        verbose_name_plural = _('Respuestas de Usuario')
        ordering = ['-modified']

    def __str__(self):
        return self.user.email


class TicketSettings(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_ticket_settings",
        on_delete=models.CASCADE, null=True)
    event_name = models.CharField(
        verbose_name=_('Nombre evento'), max_length=255, null=True)
    event_date = models.CharField(
        verbose_name=_('Fecha evento'), max_length=255, null=True)
    event_time = models.CharField(
        verbose_name=_('Hora evento'), max_length=255, null=True)
    event_address = models.CharField(
        verbose_name=_('Dirección evento'), max_length=255, null=True)
    additional_information = models.CharField(
        verbose_name=_('Información adicional'), max_length=255, null=True)

    class Meta:
        verbose_name = _('Configuración de Ticket')
        verbose_name_plural = _('Configuraciones de Ticket')

    def __str__(self):
        return self.event_name


class SurveryQuestion(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_survey_questions",
        on_delete=models.CASCADE, null=True)
    position = models.SmallIntegerField(_('Posición'), default=1)
    name = models.CharField(
        _('Nombre'),
        max_length=255)

    class Meta:
        verbose_name = _('Pregunta de Encuesta')
        verbose_name_plural = _('Preguntas de Encuesta')
        ordering = ['company', 'position']

    def __str__(self):
        return self.name

    def get_choices(self):
        return self.survey_choice_questions.filter(
            is_active=True).order_by('position')


class SurveryChoiceQuestion(BaseModel):
    question = models.ForeignKey(
        SurveryQuestion,
        related_name='survey_choice_questions',
        on_delete=models.CASCADE)
    position = models.SmallIntegerField(_('Posición'), default=1)
    name = models.CharField(
        _('Nombre'),
        max_length=255,
        blank=True,
        null=True)
    image = models.FileField(
        _('Imagen icon'),
        upload_to=get_upload_path('icons'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('Opción')
        verbose_name_plural = _('Opciones')
        ordering = ['position', '-modified']

    def __str__(self):
        if self.name:
            return self.name
        return self.question.question


class UserSurveyAnswer(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_survey_answers",
        on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(
        SurveryQuestion,
        related_name='answer_survey_questions',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    choice_question = models.ForeignKey(
        SurveryChoiceQuestion,
        related_name='answer_choice_survey_questions',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    user = models.ForeignKey(
        User,
        related_name='user_survey_answers',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Respuesta de Encuesta')
        verbose_name_plural = _('Respuestas de Encuesta')
        ordering = ['-modified']

    def __str__(self):
        return self.user.email


class NetworkingOption(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_networking_options",
        on_delete=models.CASCADE, null=True)
    name = models.CharField(
        _('Nombre'),
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Opción de Networking')
        verbose_name_plural = _('Opciones de Networking')

    def __str__(self):
        return self.name


class UserNetworkingPreference(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_user_networking_preferences",
        on_delete=models.CASCADE, null=True)
    networking_option = models.ForeignKey(
        NetworkingOption,
        related_name='networking_user_preferences',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    user = models.ForeignKey(
        User,
        related_name='networkin_preferences',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Preferencia en Networking')
        verbose_name_plural = _('Preferencias en Networking')
        ordering = ['-modified']

    def __str__(self):
        return "{}-{}".format(self.user.email, self.networking_option.name)


class FreeImage(models.Model):
    name = models.CharField(_('Nombre'), max_length=255)
    image = models.FileField(
        verbose_name=_('Imagen'),
        upload_to=get_upload_path('free_images'))

    class Meta:
        verbose_name = _('Free Image')
        verbose_name_plural = _('Free Images')

    def __str__(self):
        return self.name
