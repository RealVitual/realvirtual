from uuid import uuid4
import qrcode
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from src.apps.users.models import User
import os


class Customer(User):
    has_newsletters = models.BooleanField(_("has newsletters?"), default=False)
    has_accept_terms_conditions = models.BooleanField(
        _("accept term & conditions?"), default=True)
    is_confirmed = models.BooleanField(
        default=False, verbose_name=_('Confirmado'))
    is_guest = models.BooleanField(
        _('is guest?'),
        default=False,
    )
    confirm_code = models.CharField(
        verbose_name=_('Codigo de confirmacion'), max_length=255, null=True)

    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')
        ordering = ['-modified']

    def __str__(self):
        return '{} | {}'.format(self.email, self.names)

    def save(self, *args, **kwargs):
        if not self.confirm_code:
            self.confirm_code = str(uuid4())

        if not self.uuid_hash:
            self.uuid_hash = str(uuid4())

        super(Customer, self).save(*args, **kwargs)

    def get_name_only(self):
        name = self.names.split(' ')
        if len(name) > 1:
            return name[0]
        return self.names
