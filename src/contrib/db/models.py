from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from . import managers


class BaseModel(TimeStampedModel):
    ''' Base model with implement soft delete, created and updated fields '''

    is_active = models.BooleanField(default=True, verbose_name=_('Is active?'))

    objects = managers.SoftDeletionManager()

    all_objects = managers.SoftDeletionManager()

    class Meta:
        get_latest_by = 'modified_date'
        abstract = True

    def delete(self):
        self.hard_delete()

    def hard_delete(self):
        super(BaseModel, self).delete()


class PositionModel(models.Model):
    """ Model for position """
    position = models.IntegerField(verbose_name=_('Posición'), default=0)

    class Meta:
        verbose_name = _('Position Model')
        verbose_name_plural = _('Position Models')
        abstract = True
        ordering = ['position']


class VisibilityModel(models.Model):
    """ Model for visibility """
    is_visibility = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Visibility Model')
        verbose_name_plural = _('Visibility Models')
        abstract = True
        ordering = ['is_visibility']


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cls.objects.get(id=cache.get(cls.__name__))

    def set_cache(self):
        cache.set(self.__class__.__name__, self.pk)
