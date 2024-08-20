from django.db import models
from src.contrib.db.models import BaseModel
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ckeditor.fields import RichTextField
import os
from .constants import AccessType
from django.conf import settings


def get_upload_path(internal_folder):
    return os.path.join(
      "%s/%s/" % (settings.BUCKET_FOLDER_NAME, internal_folder))


class Company(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    domain = models.CharField(_('domain'), max_length=255, unique=True)
    logo = models.ImageField(
            _('Logo'), upload_to=get_upload_path("company"),
            null=True, blank=True)
    banner = models.ImageField(
            _('Banner'), upload_to=get_upload_path('banner'),
            null=True, blank=True)
    mobile_banner = models.ImageField(
            _('Mobile Banner'), upload_to=get_upload_path('mobile_banner'),
            null=True, blank=True)
    main_event_datetime = models.DateTimeField(_('Main event datetime'),
                                               null=True, blank=True)
    main_event_end_datetime = models.DateTimeField(_('Main event datetime'),
                                                   null=True, blank=True)
    use_filters = models.BooleanField(_('Usa filtros'), default=False)
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


class Header(TimeStampedModel):
    company = models.ForeignKey(
        Company, related_name="header",
        on_delete=models.CASCADE, null=True)
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
