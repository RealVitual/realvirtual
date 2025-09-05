import os
from enum import Enum
from django.conf import settings
import qrcode
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from src.contrib.db.models import BaseModel
from django.conf import settings
from six import StringIO
from .mixins import UidMixin
from src.apps.users.models import User
from src.apps.companies.models import Company


def get_upload_path(internal_folder):
    return os.path.join(
      "%s/%s/" % (settings.BUCKET_FOLDER_NAME, internal_folder))


class Ticket(UidMixin, BaseModel):
    class Status(Enum):
        f = "borrador"
        c = "comprado"
        e = "enviado"
        u = "usado"
    company = models.ForeignKey(
        Company, related_name="company_tickets",
        on_delete=models.CASCADE, null=True)
    code = models.CharField(
        _('Código del ticket'), max_length=8, blank=True, default='')
    hash_id = models.CharField(
        _('Hash id'), max_length=255, blank=True, null=True
    )
    qr = models.ImageField(
        verbose_name='Qr', upload_to=get_upload_path('tickets/qrcode'),
        null=True, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    document = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=200, default='', blank=True)
    status = models.CharField(
        max_length=1, blank=True,
        choices=[(item.name, item.value) for item in Status],
        default=Status.f.name)
    user = models.ForeignKey(
        User, related_name='user_tickets',
        on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(
        max_length=45, verbose_name='description', null=True, blank=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Valor Unitario del ticket", verbose_name="Valor", default=0)
    sent_date = models.DateTimeField(null=True, blank=True)
    seat = models.CharField(max_length=20, blank=True)
    seat_section = models.CharField(max_length=50, blank=True)
    is_invitation = models.BooleanField(default=False)
    number_used_code = models.PositiveIntegerField(
        verbose_name="Numero de usos", default=0
    )
    max_number_uses = models.PositiveIntegerField(
        verbose_name="Numero máximo de usos", default=0
    )
    pdf = models.FileField(
        _('PDF'),
        upload_to=get_upload_path('tickets/pdf'), null=True, blank=True)

    def get_code(self):
        return settings.HASHIDS.encode(self.id)

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.get_absolute_url())
        qr.make(fit=True)

        img = qr.make_image()

        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = 'events-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.len, None)
        self.qr.save(filename, filebuffer)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-created']


class TicketUse(models.Model):
    ticket = models.ForeignKey(
        Ticket, related_name='ticket_uses', null=True,
        on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    used_date = models.DateField(
        verbose_name="Dia Usado", blank=True, null=True)

    class Meta:
        verbose_name = "Uso de ticket"
        verbose_name_plural = "Usos de ticket"

    def __str__(self):
        return self.ticket.code
