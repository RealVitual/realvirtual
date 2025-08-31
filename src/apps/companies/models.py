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
from uuid import uuid4
from src.apps.conf.models import DocumentType, Country


def get_upload_path(internal_folder):
    return os.path.join(
      "%s/%s/" % (settings.BUCKET_FOLDER_NAME, internal_folder))


class Font(models.Model):
    name = models.CharField(_('Nombre carpeta Font'), max_length=255)

    class Meta:
        verbose_name = _("Font")
        verbose_name_plural = _("Fonts")

    def __str__(self):
        return self.name


class TemplateVersion(models.Model):
    version = models.PositiveIntegerField(_('Version de plantilla'), default=1)

    class Meta:
        verbose_name = _("Version de plantilla")
        verbose_name_plural = _("Versions de plantilla")

    def __str__(self):
        return str(self.version)


class Enterprise(models.Model):
    name = models.CharField(_('Nombre Empresa'), max_length=255)

    class Meta:
        verbose_name = _("Empresa")
        verbose_name_plural = _("Empresas")

    def __str__(self):
        return self.name


class Company(BaseModel):
    enterprise = models.ForeignKey(
        Enterprise, related_name="companies",
        on_delete=models.SET_NULL, null=True, blank=True)
    domain = models.CharField(_('dominio'), max_length=255, unique=True)
    name = models.CharField(_('Nombre compañia'), max_length=255)
    main_event_name = models.CharField(_('Nombre principal del evento'),
                                       max_length=255, blank=True, null=True)
    logo = models.FileField(
        _('Logo'), upload_to=get_upload_path("company"),
        null=True, blank=True
    )
    favicon = models.ImageField(
        _('Favicon'), upload_to=get_upload_path("favicon"),
        null=True, blank=True
    )

    use_counter = models.BooleanField(_('Usa Contador'), default=False)
    counter_datetime = models.DateTimeField(_('Fecha y Hora de contador'),
                                            null=True, blank=True)
    counter_text = models.CharField(
        _('Texto contador'), max_length=255, blank=True,
        null=True, default="Evento disponible en"
    )
    close_landing = models.BooleanField(_('Cerrar Landing'), default=False)
    close_banner = models.ImageField(
        _('Banner de cierre'), upload_to=get_upload_path('banner'),
        null=True, blank=True
    )
    close_mobile_banner = models.ImageField(
        _('Banner Mobile de cierre'),
        upload_to=get_upload_path('mobile_banner'),
        null=True, blank=True
    )

    warning_img = models.ImageField(
        _('Imagen aviso'), upload_to=get_upload_path("warning_img"),
        null=True, blank=True
    )

    version = models.ForeignKey(
        TemplateVersion, related_name="template_versions",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    font = models.ForeignKey(
        Font, related_name="css_font_companies",
        on_delete=models.SET_NULL, null=True, blank=True
    )

    banner = models.ImageField(
        _('Banner'), upload_to=get_upload_path('banner'),
        null=True, blank=True
    )
    mobile_banner = models.ImageField(
        _('Mobile Banner'), upload_to=get_upload_path('mobile_banner'),
        null=True, blank=True
    )
    image_banner = models.ImageField(
        _('Image Banner'), upload_to=get_upload_path('image_banner'),
        null=True, blank=True
    )

    banner_second_section = models.CharField(
        _('Sección Secundaria'), max_length=255, blank=True,
        null=True
    )
    banner_second_section_image = models.ImageField(
        _('Imagen de Sección Secundaria'),
        upload_to=get_upload_path('image_banner'),
        null=True, blank=True
    )
    banner_second_section_internal_title = models.CharField(
        _('Título interno de Sección Secundaria'), max_length=255, blank=True,
        null=True
    )
    banner_second_section_internal_text = models.CharField(
        _('Texto interno de Sección Secundaria'), max_length=255, blank=True,
        null=True
    )
    banner_second_section_internal_image = models.ImageField(
        _('Imagen de Sección Secundaria'),
        upload_to=get_upload_path('image_banner'),
        null=True, blank=True
    )

    banner_footer_section_image = models.ImageField(
        _('Imagen de Sección Footer'),
        upload_to=get_upload_path('image_banner'),
        null=True, blank=True
    )

    video_file = models.FileField(
        _('Video File Banner'), upload_to=get_upload_path('video_banner'),
        null=True, blank=True
    )

    main_event_datetime = models.DateTimeField(_('Main event datetime'),
                                               null=True, blank=True)
    main_event_end_datetime = models.DateTimeField(_('Main event datetime'),
                                                   null=True, blank=True)

    use_filters = models.BooleanField(_('Usa filtros'), default=False)
    use_rooms = models.BooleanField(_('Usa salas en lista'), default=False)
    use_shifts = models.BooleanField(_('Usa turnos'), default=False)
    use_dates = models.BooleanField(_('Usa fecha en lista'), default=False)

    confirm_user = models.BooleanField(_('Confirmar Usuarios'), default=False)
    message_confirm_user = RichTextField(
        _('Mensaje confirmación'), null=True, blank=True)
    title_closed_in_person_register = models.CharField(
        _('Titulo Cierre registro presencial'),
        max_length=255, null=True, blank=True
    )
    message_closed_in_person_register = models.TextField(
        _('Mensaje Cierre registro presencial'), null=True, blank=True)

    enable_credentials = models.BooleanField(_('Habilitar credenciales'),
                                             default=False)
    enable_preferences = models.BooleanField(_(
        'Habilitar selección de preferencias'), default=False)

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

    # campos formulario
    names_field_title = models.CharField(
        _('Título Nombres en Formulario'), max_length=100, default="Nombres"
    )
    last_names_field_title = models.CharField(
        _('Título Apellidos en Formulario'), max_length=100,
        default="Apellidos"
    )
    job_company_names_field_title = models.CharField(
        _('Título Empresa en Formulario'), max_length=100, default="Empresa"
    )
    company_position_names_field_title = models.CharField(
        _('Título Cargo en Formulario'), max_length=100, default="Cargo"
    )
    country_names_field_title = models.CharField(
        _('Título País en Formulario'), max_length=100, default="País"
    )
    occupation_names_field_title = models.CharField(
        _('Título Profesión en Formulario'), max_length=100,
        default="Profesión"
    )
    email_names_field_title = models.CharField(
        _('Título Email en Formulario'), max_length=100, default="Email"
    )
    confirm_email_names_field_title = models.CharField(
        _('Título Confirmar Email en Formulario'), max_length=100,
        default="Confirmar Email"
    )

    # codigos seguimiento
    code_header = models.TextField(
        _('Código seguimiento HEAD'), blank=True, null=True
    )
    code_body = models.TextField(
        _('Código seguimiento BODY'), blank=True, null=True
    )

    # Campos Formulario
    names = models.BooleanField(
        _('Nombres'), default=True)
    last_name = models.BooleanField(
        _('Apellidos'), default=True)
    job_company = models.BooleanField(
        _('Empresa / II.EE.'), default=True)
    job_company_select = models.BooleanField(
        _('Empresa / II.EE. Select'), default=False)
    company_position = models.BooleanField(
        _('Cargo / Carrera'), default=True)
    phone = models.BooleanField(
        _('Teléfono'), default=False)
    country = models.BooleanField(
        _('País'), default=True)
    occupation = models.BooleanField(
        _('Profesión'), default=True)
    occupation_select = models.BooleanField(
        _('Profesión Select'), default=False)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        if self.enterprise:
            return f'{self.enterprise.name} / {self.name}'
        return self.name

    def get_form_fields_list(self):
        fields_list = []
        if self.names:
            fields_list.append('names')
        if self.last_name:
            fields_list.append('last_name')
        if self.job_company:
            fields_list.append('job_company')
        if self.job_company_select:
            fields_list.append('job_company_select')
        if self.company_position:
            fields_list.append('company_position')
        if self.phone:
            fields_list.append('phone')
        if self.country:
            fields_list.append('country')
        if self.occupation:
            fields_list.append('occupation')
        if self.occupation_select:
            fields_list.append('occupation_select')
        return fields_list

    def set_counter_time(self):
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

    show_about_section = models.BooleanField(
        _('Mostrar Acerca de'), default=True
    )
    about_section_header_name = models.CharField(
        _('Nombre Acerca De Header'), max_length=20, default="Acerca de"
    )

    show_modules_section = models.BooleanField(
        _('Mostrar Módulos'), default=True
    )
    modules_section_header_name = models.CharField(
        _('Nombre Módulos Header'), max_length=20, default="Módulos"
    )

    schecule_header_name = models.CharField(
        _('Nombre Horario Header'), max_length=20, default="Agenda"
    )
    show_schedule_section = models.BooleanField(
        _('Mostrar Agenda'), default=True
    )

    show_gallery_section = models.BooleanField(
        _('Mostrar Galería'), default=True
    )
    gallery_header_name = models.CharField(
        _('Nombre Galería Header'), max_length=20, default="Galería"
    )

    show_sponsors_section = models.BooleanField(
        _('Mostrar Auspiciadores'), default=True
    )
    sponsors_header_name = models.CharField(
        _('Nombre Auspiciadores Header'), max_length=20,
        default="Auspiciadores"
    )

    show_networking_section = models.BooleanField(
        _('Mostrar Networking'), default=True
    )
    networking_header_name = models.CharField(
        _('Nombre Networking Header'), max_length=20, default="Networking"
    )

    show_survey_section = models.BooleanField(
        _('Mostrar Encuesta'), default=True
    )
    survey_header_name = models.CharField(
        _('Nombre Encuesta Header'), max_length=20, default="Encuesta"
    )

    show_more_events = models.BooleanField(
        _('Mostrar Más eventos'), default=True
    )

    show_exhibitors_section = models.BooleanField(
        _('Mostrar Expositores'), default=True
    )
    exhibitors_header_name = models.CharField(
        _('Nombre Expositores Header'), max_length=20, default="Expositores"
    )

    show_blog_section = models.BooleanField(
        _('Mostrar Blog'), default=True
    )
    blog_header_name = models.CharField(
        _('Nombre Blog Header'), max_length=20, default="Blog"
    )

    show_contact = models.BooleanField(
        _('Mostrar Contacto en Header'), default=False
    )
    contact_header_name = models.CharField(
        _('Nombre Contacto Header'), max_length=50, default="Contacto"
    )

    show_workshops_section = models.BooleanField(
        _('Mostrar Talleres'), default=True
    )
    workshops_header_name = models.CharField(
        _('Nombre Talleres Header'), max_length=20, default="Talleres"
    )

    show_frequently_questions_section = models.BooleanField(
        _('Mostrar Preguntas Frecuentes'), default=True
    )
    frequently_questions_header_name = models.CharField(
        _('Nombre Preguntas Frecuentes Header'), max_length=20,
        default="Preguntas Frecuentes"
    )

    register_title = models.CharField(
        _('Título Registro'), max_length=50, default="Regístrate"
    )
    register_form_title = models.CharField(
        _('Título Registro Formulario'), max_length=255, default="Crear cuenta"
    )
    register_form_text = models.TextField(
        _('Texto Registro Formulario'),
        default="Completa el siguiente formulario para poder registrar tus datos." # noqa
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
    background = models.CharField(
        'Background Color', max_length=100, default="#333")
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
    youtube = models.URLField(
        _('Youtube'), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Footer")
        verbose_name_plural = _("Footers")

    def __str__(self):
        return f'Footer for {self.company}'

    def mobile_link(self):
        if self.mobile:
            return self.mobile.replace(" ", "")
        return ""


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

    home_video_url = models.CharField(
            _('Home Video Url'), max_length=255, null=True, blank=True)
    banner = models.ImageField(
        _('Banner'), upload_to=get_upload_path('banner'),
        null=True, blank=True
    )
    mobile_banner = models.ImageField(
        _('Mobile Banner'), upload_to=get_upload_path('mobile_banner'),
        null=True, blank=True
    )
    image_banner = models.ImageField(
        _('Image Banner'), upload_to=get_upload_path('image_banner'),
        null=True, blank=True
    )

    banner_second_section = models.CharField(
        _('Sección Secundaria'), max_length=255, blank=True,
        null=True
    )
    banner_second_section_image = models.ImageField(
        _('Imagen de Sección Secundaria'),
        upload_to=get_upload_path('image_banner'),
        null=True, blank=True
    )
    banner_second_section_internal_title = models.CharField(
        _('Título interno de Sección Secundaria'), max_length=255, blank=True,
        null=True
    )
    banner_second_section_internal_text = models.CharField(
        _('Texto interno de Sección Secundaria'), max_length=255, blank=True,
        null=True
    )
    banner_second_section_internal_image = models.ImageField(
        _('Imagen Interna de Sección Secundaria'),
        upload_to=get_upload_path('image_banner'),
        null=True, blank=True
    )
    video_file = models.FileField(
        _('Video File Banner'), upload_to=get_upload_path('video_banner'),
        null=True, blank=True
    )

    first_title = models.CharField(
            _('First Title'), max_length=255, null=True, blank=True)
    main_title = models.CharField(
            _('Main Title'), max_length=255, null=True, blank=True)
    secondary_title = models.CharField(
            _('Secondary Title'), max_length=255, null=True, blank=True)
    address_description = models.CharField(
        _('Address description'), max_length=50, blank=True, null=True
    )
    date_description = models.CharField(
        _('Date description'), max_length=50, blank=True, null=True
    )
    time_description = models.CharField(
        _('Time description'), max_length=50, blank=True, null=True
    )
    banner_description = models.TextField(
        _('Description'), blank=True, null=True
    )
    banner_footer_section_image = models.ImageField(
        _('Imagen de Sección Footer'),
        upload_to=get_upload_path('image_banner'),
        null=True, blank=True
    )

    main_event_title = models.CharField(
        _('Detalle Evento Título'), max_length=255, blank=True)
    main_event_sub_title = models.CharField(
        _('Detalle Evento Subtítulo'), max_length=255, blank=True)
    main_event_description = models.TextField(
        _('Detalle Evento Description'), blank=True)
    main_event_video_url = models.CharField(
            _('Detalle Evento Video Url'), max_length=255, null=True, blank=True)
    main_event_image = models.ImageField(
            _('Detalle Evento image'),
            upload_to=get_upload_path('main_event_image'),
            null=True, blank=True)

    module_section_name = models.CharField(
        _('Módulos nombre Sección'), max_length=255,
        blank=True, default="Módulos")
    module_section_title = models.CharField(
        _('Módulos título Sección'), max_length=255,
        blank=True, default="Programas y Ponentes")
    module_section_text = models.TextField(
        _('Módulos texto Sección'), blank=True)

    schedule_section_name = models.CharField(
        _('Agenda nombre Sección'), max_length=255,
        blank=True, default="Agenda")
    schedule_section_title = models.CharField(
        _('Agenda título Sección'), max_length=255,
        blank=True, default="Programas y Ponentes")

    exhibitors_section_name = models.CharField(
        _('Expositores nombre Sección'), max_length=255,
        blank=True, default="Expositores")
    exhibitors_section_title = models.CharField(
        _('Expositores título Sección'), max_length=255,
        blank=True, default="Conoce a los expositores")

    blog_section_name = models.CharField(
        _('Blog nombre Sección'), max_length=255,
        blank=True, default="NOVEDADES")
    blog_section_title = models.CharField(
        _('Blog título Sección'), max_length=255,
        blank=True, null=True)
    blog_button_title = models.CharField(
        _('Blog título botón Sección'), max_length=255,
        blank=True, default="Visitar Blog")

    sponsors_section_name = models.CharField(
        _('Auspiciadores nombre Sección'), max_length=255,
        blank=True, default="Empresa")
    sponsors_section_text = models.CharField(
        _('Auspiciadores texto'), max_length=255,
        blank=True, default="Con la participación de")

    gallery_section_name = models.CharField(
        _('Galería nombre Sección'), max_length=255,
        blank=True, default="Empresa")
    gallery_section_text = models.CharField(
        _('Galería texto'), max_length=255,
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

    workshop_section_name = models.CharField(
        _('Talleres nombre Sección'), max_length=255,
        blank=True, default="Talleres")
    workshop_section_image = models.ImageField(
            _('Detalle Talleres image'),
            upload_to=get_upload_path('workshop_image'),
            null=True, blank=True)

    frequently_questions_section_name = models.CharField(
        _('Preguntas Frecuentes nombre Sección'), max_length=255,
        blank=True, default="Preguntas Frecuentes")

    final_image = models.ImageField(
        _('Imagen Sección final'),
        upload_to=get_upload_path('final_image'),
        null=True, blank=True
    )

    class Meta:
        verbose_name = _("Home Page")
        verbose_name_plural = _("Home Pages")

    def __str__(self):
        return f'home for {self.company}'

    def get_items(self):
        return self.main_event_items.order_by('position')

    def get_indicators(self):
        return self.main_event_indicators.order_by('position')

    def get_modules(self):
        return self.items_modules.order_by('position')


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


class IndicatorsMainEvent(BaseModel):
    home_page = models.ForeignKey(
        HomePage, related_name="main_event_indicators",
        on_delete=models.CASCADE)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    title = models.CharField(
            _('Título'), max_length=255, null=True, blank=True)
    number = models.CharField(
            _('Número'), default=1, null=True, blank=True)

    class Meta:
        verbose_name = _('Indicador')
        verbose_name_plural = _('Indicadores')
        ordering = ('position', )

    def __str__(self):
        return f'Indicador for {self.home_page}'


class ItemModule(BaseModel):
    home_page = models.ForeignKey(
        HomePage, related_name="items_modules",
        on_delete=models.CASCADE)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    title = models.CharField(
            _('Title'), max_length=255, null=True, blank=True)
    description = models.TextField(
        _('Description'), null=True, blank=True)
    image = models.ImageField(
            _('Imagen'), upload_to=get_upload_path("module"),
            null=True, blank=True
        )

    class Meta:
        verbose_name = _('Item Module')
        verbose_name_plural = _('Items Modules')
        ordering = ('position', )

    def __str__(self):
        return f'item module for {self.home_page}'


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
        if self.username and self.company:
            return f'{self.company.name} - {self.username}'
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
    description = models.TextField("Descripción", blank=True, null=True)
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
        if self.email_type and self.company:
            return f'{self.email_type} - {self.company}'
        return "Email template"


class JobCompany(BaseModel):
    company = models.ForeignKey(
        Company, related_name="job_companies",
        on_delete=models.CASCADE)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=0)
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _("Empresa de trabajo")
        verbose_name_plural = _("Empresas de trabajo")
        ordering = ['position', 'name']

    def __str__(self):
        return self.name


class Occupation(BaseModel):
    company = models.ForeignKey(
        Company, related_name="occupations",
        on_delete=models.CASCADE)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=0)
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _("Profesión")
        verbose_name_plural = _("Profesiones")
        ordering = ['position', 'name']

    def __str__(self):
        return self.name


class UserCompany(BaseModel):
    is_admin = models.BooleanField(_('Es admin'), default=False)
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
    virtual = models.BooleanField(_('Virtual'), default=False)
    in_person = models.BooleanField(_('In Person'), default=False)
    allow_networking = models.BooleanField(
        _('Allow Networking'), default=False)
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
    phone = models.CharField(_('phone'), max_length=50, null=True, blank=True)
    mobile = models.CharField(
        _('mobile'), max_length=50, null=True, blank=True)
    document_type = models.ForeignKey(
        DocumentType, related_name="%(class)s_set",
        on_delete=models.CASCADE, null=True, blank=True)
    document = models.CharField(
        _("document"), max_length=120, null=True, blank=True)
    occupation = models.CharField(
        'Profesion ', max_length=255, blank=True, null=True)
    occupation_select = models.ForeignKey(
        Occupation, verbose_name="Profesion",
        related_name="occupation_company_users",
        on_delete=models.SET_NULL, null=True, blank=True)
    job_company = models.CharField(
        'Empresa / II.EE.', max_length=255, blank=True, null=True)
    job_company_select = models.ForeignKey(
        JobCompany, verbose_name="Empresa",
        related_name="job_company_company_users",
        on_delete=models.SET_NULL, null=True, blank=True)
    company_position = models.CharField(
        'Cargo / Carrera', max_length=255, blank=True, null=True)
    speciality = models.ForeignKey(
        'conf.Speciality', related_name="specialities_company_users",
        on_delete=models.DO_NOTHING, null=True, blank=True)
    country = models.ForeignKey(
        Country, related_name="country_company_users",
        on_delete=models.SET_NULL, null=True, blank=True)
    allow_certificate = models.BooleanField(_('Permitir certificado'), default=False)
    certificate = models.FileField(
        _('certificate'),
        upload_to=get_upload_path('certificates'),
        null=True, blank=True)


    uuid_hash = models.CharField(
        'UUID',
        max_length=36,
        default='',
        blank=True,
        help_text=_('Random UUID hash to recover password.'))

    class Meta:
        unique_together = ('company', 'email')
        verbose_name = _('Usuario de Compañía')
        verbose_name_plural = _('Usuarios de Compañías')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

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

    def name_only(self):
        name = self.names.split(' ')
        if len(name) > 1:
            return name[0]
        return name

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.uuid_hash:
            self.uuid_hash = str(uuid4())
        if not self.full_name:
            self.full_name = f'{self.names} {self.last_name}'
        super(UserCompany, self).save(*args, **kwargs)
