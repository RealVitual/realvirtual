import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from src.contrib.db.models import BaseModel
from src.apps.companies.models import Company
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.conf import settings


def get_upload_path(internal_folder):
    return os.path.join(
      "%s/%s/" % (settings.BUCKET_FOLDER_NAME, internal_folder))


class Event(BaseModel):
    company = models.ForeignKey(
        Company, related_name="events",
        on_delete=models.CASCADE, null=True)
    name = models.CharField(
        _('Name'), max_length=255, blank=True)
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
        return f'home for {self.company}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    def get_schedules(self):
        return self.schedules.filter(is_active=True).order_by('start_time')


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
    description = models.TextField(
        _('Descripcion'), blank=True)
    image = models.ImageField(
        _('Imagen'), upload_to=get_upload_path('exhibitors'), blank=True,
        null=True)
    link = models.CharField(
        _('Enlace'), blank=True, max_length=500)

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

    class Meta:
        verbose_name = _('Horario')
        verbose_name_plural = _('Horarios')
        ordering = ('start_time', )

    def __str__(self):
        return "{}".format(self.name)
