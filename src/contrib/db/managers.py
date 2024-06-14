from django.db import models

from .querysets import SoftDeletionQuerySet


class SoftDeletionManager(models.Manager):
    ''' Manager to implement soft delete '''

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        # if self.alive_only:
        #     return SoftDeletionQuerySet(self.model).filter(is_active=True)
        return SoftDeletionQuerySet(self.model)

    def delete(self):
        return self.get_queryset().delete()

    def hard_delete(self):
        return self.get_queryset().hard_delete()
