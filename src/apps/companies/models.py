from django.db import models
from src.contrib.db.models import BaseModel
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ckeditor.fields import RichTextField
import os
from .constants import AccessType
from django.conf import settings
from .constants import (
    EmailType, )
from django.contrib.auth.hashers import make_password, check_password
from src.apps.users.models import User


def get_upload_path(internal_folder):
    return os.path.join(
      "%s/%s/" % (settings.BUCKET_FOLDER_NAME, internal_folder))


class Company(BaseModel):
    name = models.CharField(_('Nombre compañia'), max_length=255)
    main_event_name = models.CharField(_('Nombre principal del evento'),
                                       max_length=255, blank=True, null=True)
    domain = models.CharField(_('dominio'), max_length=255, unique=True)
    counter_datetime = models.DateTimeField(_('Fecha y Hora de contador'),
                                            null=True, blank=True)
    use_counter = models.BooleanField(_('Usa Contador'), default=False)
    counter_text = models.CharField(
        _('Texto contador'), max_length=255, blank=True,
        null=True, default="Evento disponible en")
    logo = models.ImageField(
            _('Logo'), upload_to=get_upload_path("company"),
            null=True, blank=True)
    favicon = models.ImageField(
            _('Favicon'), upload_to=get_upload_path("favicon"),
            null=True, blank=True)
    banner = models.ImageField(
            _('Banner'), upload_to=get_upload_path('banner'),
            null=True, blank=True)
    mobile_banner = models.ImageField(
            _('Mobile Banner'), upload_to=get_upload_path('mobile_banner'),
            null=True, blank=True)
    video_file = models.FileField(
            _('Video File Banner'), upload_to=get_upload_path('video_banner'),
            null=True, blank=True)
    main_event_datetime = models.DateTimeField(_('Main event datetime'),
                                               null=True, blank=True)
    main_event_end_datetime = models.DateTimeField(_('Main event datetime'),
                                                   null=True, blank=True)
    use_filters = models.BooleanField(_('Usa filtros'), default=False)
    use_rooms = models.BooleanField(_('Usa salas en lista'), default=False)
    use_shifts = models.BooleanField(_('Usa turnos'), default=False)
    use_dates = models.BooleanField(_('Usa fecha en lista'), default=False)
    enable_credentials = models.BooleanField(_('Habilitar credenciales'),
                                             default=False)
    privacy_policy = models.FileField(
            _('Políticas de privacidad'),
            upload_to=get_upload_path('documents'),
            null=True, blank=True)
    protection_data_policy = models.FileField(
            _('Políticas de Protección de datos'),
            upload_to=get_upload_path('documents'),
            null=True, blank=True)
    cookies_policy = models.FileField(
            _('Políticas Cookies'),
            upload_to=get_upload_path('documents'),
            null=True, blank=True)
    terms_and_conditions = models.FileField(
            _('Términos y condiciones'),
            upload_to=get_upload_path('documents'),
            null=True, blank=True)
    is_virtual = models.BooleanField(_('Is virtual'), default=True)
    in_person = models.BooleanField(_('In Person'), default=False)
    is_private = models.BooleanField(_('Is Private'), default=False)
    access_type = models.CharField(
        _('access type'),
        choices=AccessType.choices(),
        max_length=30,
        default=AccessType.VIRTUAL)
    allow_virtual_access = models.BooleanField(
        _('Allow virtual access'), default=True)
    capacity = models.PositiveIntegerField(_('Capacity'), default=500)
    current_quantity = models.PositiveIntegerField(
        _('Current quantity'), default=0)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name

    def set_counter_time(self):
        print(self.counter_datetime.strftime('%d-%m-%Y %H:%M:%S'))
        return self.counter_datetime.strftime('%d-%m-%Y %H:%M:%S')


class Header(TimeStampedModel):
    company = models.ForeignKey(
        Company, related_name="header",
        on_delete=models.CASCADE, null=True)
    header_color = models.CharField(
        _('Header color'), max_length=20, default="#FFFFF"
    )
    header_text_color = models.CharField(
        _('Header texto color'), max_length=20, default="#17181b"
    )
    button_color = models.CharField(
        _('Header botón color'), max_length=20, default="#008ac9"
    )
    button_text_color = models.CharField(
        _('Header texto botón color'), max_length=20, default="#FFFFF"
    )
    about_section_header_name = models.CharField(
        _('Nombre Acerca De Header'), max_length=20, default="Acerca de"
    )
    show_about_section = models.BooleanField(
        _('Mostrar Acerca de'), default=True
    )
    schecule_header_name = models.CharField(
        _('Nombre Horario Header'), max_length=20, default="Agenda"
    )
    show_schedule_section = models.BooleanField(
        _('Mostrar Agenda'), default=True
    )
    gallery_header_name = models.CharField(
        _('Nombre Galería Header'), max_length=20, default="Galería"
    )
    show_gallery_section = models.BooleanField(
        _('Mostrar Galería'), default=True
    )
    sponsors_header_name = models.CharField(
        _('Nombre Auspiciadores Header'), max_length=20,
        default="Auspiciadores"
    )
    show_sponsors_section = models.BooleanField(
        _('Mostrar Auspiciadores'), default=True
    )
    networking_header_name = models.CharField(
        _('Nombre Networking Header'), max_length=20, default="Networking"
    )
    show_networking_section = models.BooleanField(
        _('Mostrar Networking'), default=True
    )
    survey_header_name = models.CharField(
        _('Nombre Encuesta Header'), max_length=20, default="Encuesta"
    )
    show_survey_section = models.BooleanField(
        _('Mostrar Encuesta'), default=True
    )
    show_more_events = models.BooleanField(
        _('Mostrar Más eventos'), default=True
    )
    exhibitors_header_name = models.CharField(
        _('Nombre Expositores Header'), max_length=20, default="Expositores"
    )
    show_exhibitors_section = models.BooleanField(
        _('Mostrar Expositores'), default=True
    )
    register_title = models.CharField(
        _('Título Registro'), max_length=20, default="Regístrate"
    )
    login_title = models.CharField(
        _('Título Login'), max_length=20, default="Inicia Sesión"
    )

    class Meta:
        verbose_name = _("Header")
        verbose_name_plural = _("Headers")

    def __str__(self):
        return f'Header for {self.company}'


class Footer(TimeStampedModel):
    company = models.ForeignKey(
        Company, related_name="footer",
        on_delete=models.CASCADE, null=True)
    text = models.CharField('Texto', max_length=255, blank=True, null=True)
    mobile = models.CharField(
            _('Número teléfono'), max_length=255, null=True, blank=True)
    facebook = models.URLField(
            _('Facebook'), max_length=255, null=True, blank=True)
    instagram = models.URLField(
        _('Instagram'), max_length=255, blank=True, null=True
    )
    twitter = models.URLField(
        _('Twitter'), max_length=255, blank=True, null=True
    )
    linkedin = models.URLField(
        _('Linkedin'), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Footer")
        verbose_name_plural = _("Footers")

    def __str__(self):
        return f'Footer for {self.company}'


class HomePage(TimeStampedModel):
    company = models.ForeignKey(
        Company, related_name="home_company",
        on_delete=models.CASCADE, null=True)
    buttons_color = models.CharField(
        _('Botones color'), max_length=20, default="#008ac9"
    )
    text_buttons_color = models.CharField(
        _('Texto en Botones color'), max_length=20, default="#FFFFFF"
    )
    home_banner = models.ImageField(
            _('Home Banner'), upload_to=get_upload_path('banner'),
            null=True, blank=True)
    home_video_url = models.CharField(
            _('Home Video Url'), max_length=255, null=True, blank=True)
    first_title = models.CharField(
            _('First Title'), max_length=255, null=True, blank=True)
    main_title = models.CharField(
            _('Main Title'), max_length=255, null=True, blank=True)
    secondary_title = models.CharField(
            _('Secondary Title'), max_length=255, null=True, blank=True)
    date_description = models.CharField(
        _('Date description'), max_length=50, blank=True, null=True
    )
    time_description = models.CharField(
        _('Time description'), max_length=50, blank=True, null=True
    )
    main_event_title = models.CharField(
        _('Main Event title'), max_length=255, blank=True)
    main_event_description = models.TextField(
        _('Main Event Description'), blank=True)
    main_event_video_url = models.CharField(
            _('Main Event Video Url'), max_length=255, null=True, blank=True)
    main_event_image = models.ImageField(
            _('Main Event image'),
            upload_to=get_upload_path('main_event_image'),
            null=True, blank=True)
    schedule_section_name = models.CharField(
        _('Agenda nombre Sección'), max_length=255,
        blank=True, default="Agenda")
    schedule_section_title = models.CharField(
        _('Agenda título Sección'), max_length=255,
        blank=True, default="Programas y Ponentes")
    exhibitors_section_name = models.CharField(
        _('Expositores nombre Sección'), max_length=255,
        blank=True, default="Expositores")
    sponsors_section_name = models.CharField(
        _('Auspiciadores nombre Sección'), max_length=255,
        blank=True, default="Empresa")
    sponsors_section_text = models.CharField(
        _('Auspiciadores texto'), max_length=255,
        blank=True, default="Con la participación de")
    networking_section_name = models.CharField(
        _('Networking nombre Sección'), max_length=255,
        blank=True, default="Networking")
    networking_description_text = models.CharField(
        _('Networking descripción texto'), max_length=255,
        blank=True, default="Conéctate con los demás usuarios.")
    survey_section_name = models.CharField(
        _('Encuesta nombre Sección'), max_length=255,
        blank=True, default="Tu opinión es importante")
    survey_description_text = models.CharField(
        _('Encuesta descripción texto'), max_length=255,
        blank=True,
        default="Por favor, ayúdanos a mejorar nuestra atención completando la siguiente encuesta.") # noqa

    class Meta:
        verbose_name = _("Home Page")
        verbose_name_plural = _("Home Pages")

    def __str__(self):
        return f'home for {self.company}'

    def get_items(self):
        return self.main_event_items.order_by('position')


class ItemMainEvent(BaseModel):
    home_page = models.ForeignKey(
        HomePage, related_name="main_event_items",
        on_delete=models.CASCADE)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    title = models.CharField(
            _('Title'), max_length=255, null=True, blank=True)
    description = RichTextField(
        _('Description'), null=True, blank=True)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        ordering = ('position', )

    def __str__(self):
        return f'item for {self.home_page}'


class EmailSettings(BaseModel):
    company = models.ForeignKey(
        Company, related_name="email_settings",
        on_delete=models.DO_NOTHING, null=True, blank=True)
    host = models.CharField(
        "Email Host", max_length=500, blank=True, null=True)
    port = models.CharField(
        "Email Port", max_length=500, default=587)
    username = models.CharField(
        "Username Email", max_length=500, blank=True, null=True)
    password = models.CharField(
        "Password Email", max_length=500, blank=True, null=True)
    use_tls = models.BooleanField(_('Usa TLS'), default=True)
    schedule_mail = models.BooleanField(
        _('Enviar correo de agenda'), default=True)
    register_mail = models.BooleanField(
        _('Enviar correo de registro'), default=True)

    class Meta:
        verbose_name = _('Reglas de correo')
        verbose_name_plural = _('Reglas de correo')

    def __str__(self):
        return "Reglas de correo"


class EmailTemplate(BaseModel):
    company = models.ForeignKey(
        Company, related_name="email_templates",
        on_delete=models.DO_NOTHING, null=True, blank=True)
    email_type = models.CharField(
        verbose_name=_('¿Para qué se usará el correo?'),
        max_length=30, choices=EmailType.choices(),
        default=EmailType.REGISTER)
    name = models.CharField(
        'Nombre', max_length=200, null=True)
    subject = models.CharField("Asunto", max_length=128)
    html_code = models.TextField('Código HTML', blank=True)
    from_email = models.EmailField(
        _('Email Emisor'), null=True, blank=True)
    from_name = models.CharField(
            _('Nombre Emisor'), null=True, blank=True,
            max_length=255)
    attach_file = models.BooleanField(_('Tiene adjunto'), default=False)

    class Meta:
        verbose_name = _('Plantilla Correo')
        verbose_name_plural = _('Plantillas Correo')

    def __str__(self):
        return f'{self.email_type} - {self.company}'


class UserCompany(models.Model):
    email = models.EmailField()
    company = models.ForeignKey(Company, related_name="company_users",
                                on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    user = models.ForeignKey(
        User, related_name="user_companies",
        on_delete=models.SET_NULL, null=True, blank=True)
    confirmed = models.BooleanField(
        _('email confirmed?'),
        default=True)

    class Meta:
        unique_together = ('company', 'email')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
