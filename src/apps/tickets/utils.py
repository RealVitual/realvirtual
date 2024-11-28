from io import BytesIO
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Ticket
from src.apps.companies.models import UserCompany


def generate_ticket_code(user=None, company=None):
    ticket = Ticket()
    if user:
        user_company = UserCompany.objects.get(user=user, company=company)
        existing_tickets = Ticket.objects.filter(user=user, company=company) # noqa
        if existing_tickets:
            ticket = existing_tickets.last()
            ticket.full_name = user_company.full_name
            ticket.save()
            return ticket
        ticket.user = user
        ticket.email = user.email
        ticket.full_name = user.full_name
        ticket.document = user.document if user.document else ""
    ticket.company = company
    ticket.status = "c"
    ticket.save()
    ticket.code = ticket.get_code()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    data = '{}'.format(ticket.code)

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    buffer = BytesIO()
    img.save(buffer)
    filename = 'ticket-%s.png' % ticket.id
    filebuffer = InMemoryUploadedFile(
        buffer, None, filename, 'image/png', None, None)
    ticket.qr.save(filename, filebuffer)
    ticket.save()
    return ticket
