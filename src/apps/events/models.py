import os
import pytz
from django.db import models
from django.utils.translation import gettext_lazy as _
from src.contrib.db.models import BaseModel
from src.apps.companies.models import Company, UserCompany
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.conf import settings
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey
from src.apps.users.models import User
from src.contrib.db.models import BaseModel


def get_upload_path(internal_folder):
    return os.path.join(
      "%s/%s/" % (settings.BUCKET_FOLDER_NAME, internal_folder))


class Room(BaseModel):
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    name = models.CharField(max_length=100, unique=True)
    filter_name = models.SlugField(
        _('Filter name'),
        max_length=450,
        blank=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sala")
        verbose_name_plural = _("Salas")
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.filter_name:
            self.filter_name = slugify(self.name)
        super(Room, self).save(*args, **kwargs)


class Shift(BaseModel):
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    name = models.CharField(max_length=100, unique=True)
    filter_name = models.SlugField(
        _('Filter name'),
        max_length=450,
        blank=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Turno")
        verbose_name_plural = _("Turnos")
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.filter_name:
            self.filter_name = slugify(self.name)
        super(Shift, self).save(*args, **kwargs)


class Filter(BaseModel):
    company = models.ForeignKey(
        Company, related_name="filters",
        on_delete=models.CASCADE, null=True)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    filter_name = models.SlugField(
        _('Filter name'),
        max_length=450,
        blank=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Filter")
        verbose_name_plural = _("Filters")
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.filter_name:
            self.filter_name = slugify(self.name)
        super(Filter, self).save(*args, **kwargs)

    def ordered_categories(self):
        return self.filter_categories.order_by('position')


class Category(MPTTModel):
    company = models.ForeignKey(
        Company, related_name="categories",
        on_delete=models.CASCADE, null=True)
    filter = models.ForeignKey(
        Filter, related_name="filter_categories",
        on_delete=models.DO_NOTHING, null=True)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True,
                            related_name='sub_categories')
    filter_name = models.SlugField(
        _('Filter name'),
        max_length=450,
        blank=True, editable=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        if self.filter:
            return f"{self.filter.name} - {self.name}"
        return f"{self.company.name} - {self.name}"

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.filter_name:
            self.filter_name = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Event(BaseModel):
    company = models.ForeignKey(
        Company, related_name="events",
        on_delete=models.CASCADE, null=True)
    name = models.CharField(
        _('Name'), max_length=255, blank=True)
    subtitle = models.CharField(
        _('Sub title'), max_length=255, blank=True)
    start_datetime = models.DateTimeField(_('Start Datetime'))
    end_datetime = models.DateTimeField(_('End Datetime'))
    description = RichTextField(
        _('description'), null=True, blank=True)
    main_img = models.ImageField(
        _('Imagen Principal'),
        upload_to=get_upload_path('main_image'), null=True, blank=True)
    video_url = models.URLField(
        _('Video URL'), blank=True, null=True)
    slug = models.SlugField(
        _('Url'),
        max_length=450,
        blank=True, editable=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    def get_schedules(self):
        return self.schedules.filter(is_active=True).order_by('start_time')

    def get_date(self):
        months = {
            "January": "Enero", "February": "Febrero",
            "March": "Marzo", "April": "Abril",
            "May": "Mayo", "June": "Junio", "July": "Julio",
            "August": "Agosto", "September": "Setiembre",
            "October": "Octubre", "November": "Noviembre",
            "December": "Diciembre"
        }
        date = self.start_datetime.astimezone(pytz.timezone(settings.TIME_ZONE)) # noqa
        month = months.get(date.strftime("%B"))
        start_date = date.strftime("%d de {}".format(month))
        return start_date


class Exhibitor(BaseModel):
    company = models.ForeignKey(
        Company, related_name="exhibitors",
        on_delete=models.CASCADE, null=True)
    position = models.PositiveIntegerField(
        _('Posición'),
        default=1)
    name = models.CharField(
        _('Nombre'), max_length=255, blank=True)
    title = models.CharField(
        _('Título'), max_length=255, blank=True)
    name_on_list = models.CharField(
        _('Nombre en lista'), max_length=100, blank=True, null=True
    )
    description = models.TextField(
        _('Descripcion'), blank=True)
    image = models.ImageField(
        _('Imagen'), upload_to=get_upload_path('exhibitors'), blank=True,
        null=True)
    flag_image = models.ImageField(
        _('Bandera Imagen'), upload_to=get_upload_path('flags'), blank=True,
        null=True)
    link = models.CharField(
        _('Enlace'), blank=True, max_length=500)
    organization = models.CharField(
        _('Organización'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Expositor')
        verbose_name_plural = _('Expositores')
        ordering = ('position', )

    def __str__(self):
        return "{}-{}".format(self.name, self.link)


class Schedule(BaseModel):
    event = models.ForeignKey(
        Event, related_name="schedules",
        on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category,
                                        related_name='category_eventos',
                                        blank=True,
                                        null=True)
    start_time = models.TimeField(
        _('Start time'), null=True, blank=True)
    end_time = models.TimeField(
        _('End time'), null=True, blank=True)
    name = models.CharField(
        _('Nombre'), max_length=255, blank=True)
    description = models.TextField(
        _('Descripcion'), blank=True)
    exhibitors = models.ManyToManyField(
        Exhibitor, related_name='schedule_exhibitors', blank=True, null=True)
    image = models.ImageField(
        _('Imagen'), upload_to=get_upload_path('schedules'), blank=True,
        null=True)
    video_url = models.URLField(
        _('Video URL'), blank=True, null=True)
    room = models.ForeignKey(
        Room, related_name="room_schedules",
        on_delete=models.DO_NOTHING, null=True, blank=True)
    shift = models.ForeignKey(
        Shift, related_name="shift_schedules",
        on_delete=models.DO_NOTHING, null=True, blank=True)
    ics_file = models.FileField(
        'ICS File', upload_to=get_upload_path("ics_files"), null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Horario')
        verbose_name_plural = _('Horarios')
        ordering = ('start_time', )

    def __str__(self):
        return "{} - ({})".format(self.name, self.event.name)

    def get_exhibitors(self):
        return self.exhibitors.all()

    def get_date(self):
        months = {
            "January": "Enero", "February": "Febrero",
            "March": "Marzo", "April": "Abril",
            "May": "Mayo", "June": "Junio", "July": "Julio",
            "August": "Agosto", "September": "Setiembre",
            "October": "Octubre", "November": "Noviembre",
            "December": "Diciembre"
        }
        # days = {
        #     "Sunday": "Domingo", "Monday": "Lunes",
        #     "Tuesday": "Martes", "Wednesday": "Miércoles",
        #     "Thursday": "Jueves", "Friday": "Viernes",
        #     "Saturday": "Sábado"
        # }
        date = self.event.start_datetime.astimezone(
            pytz.timezone(settings.TIME_ZONE))
        month = months.get(date.strftime("%B"))
        # day = days.get(date.strftime("%A"))
        return date.strftime("%d de {}".format(month.lower()))

    def get_current_status(self):
        start_date = self.event.start_datetime.date()
        end_date = self.event.end_datetime.date()
        start_time = self.start_time
        end_time = self.end_time
        start_datetime = datetime.combine(
            start_date, start_time).astimezone(pytz.utc)
        end_datetime = datetime.combine(
            end_date, end_time).astimezone(pytz.utc)
        now = datetime.now().replace(microsecond=0)
        now = now.astimezone(pytz.utc)
        status = ''
        if now >= start_datetime and end_datetime > now:
            status = 'is_live'
        if end_datetime < now:
            status = 'past'
        if start_datetime > now:
            status = 'upcoming'
        return status


class ScheduleCustomerEvent(BaseModel):
    company = models.ForeignKey(
        Company, related_name="company_customer_schedules",
        on_delete=models.CASCADE)
    company_user = models.ForeignKey(
        UserCompany, related_name="company_user_schedules",
        on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(
        Event, related_name="schedule_event_company_users",
        verbose_name=_('Evento'),
        on_delete=models.CASCADE)
    schedule = models.ForeignKey(
        Schedule, related_name="schedule_company_users",
        verbose_name=_('Schedule'),
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Horario Agendado')
        verbose_name_plural = _('Horarios Agendados')
        ordering = ['-modified']

    def __str__(self):
        return self.company_user.email


class CustomerEvent(BaseModel):
    company_user = models.ForeignKey(
        UserCompany, related_name="company_user_events",
        on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(
        Event, related_name="event_company_users", on_delete=models.DO_NOTHING,
        blank=True, null=True
    )

    class Meta:
        verbose_name = _('Asistencias de usuario')
        verbose_name_plural = _('Asistencia de usuario')
        ordering = ['-modified']

    def __str__(self):
        return '{} | {}'.format(
            self.company_user.email, self.event.name)
