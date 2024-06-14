from django.db import models


class SoftDeletionQuerySet(models.QuerySet):
    ''' Redefinition of Queryset methods to handle soft delete '''

    def delete(self):
        # return super(SoftDeletionQuerySet, self).update(is_active=False)
        return super(SoftDeletionQuerySet, self).delete()

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(is_active=False)

    def dead(self):
        return self.exclude(is_active=False)
