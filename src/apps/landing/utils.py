from .models import TicketSettings, CredentialSettings
from django.template import Context, Template
from django.utils.safestring import mark_safe
from pyvirtualdisplay import Display
import imgkit
import base64
import hashlib
from src.apps.companies.models import Company, UserCompany
from src.apps.landing.models import CerficateSettings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.core.files import File
from io import BytesIO
from weasyprint.text.fonts import FontConfiguration


def decode_base64_file(data, file_name):

    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    from django.core.files.base import ContentFile
    import base64
    import six
    import uuid

    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        if not file_name:
            file_name = str(uuid.uuid4())[:12]
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension, )

        return ContentFile(decoded_file, name=complete_file_name)


def hasherStr(texto):
    hash_object = hashlib.sha1(texto.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return str(hex_dig)[10:35:2]


def generate_credential(instance, company, full_credential_name):
    template_object = CredentialSettings.objects.get(company=company)
    template = Template(mark_safe(template_object.html_code))
    context = dict(customer=instance)
    html_content = template.render(Context(context))
    # display = Display(visible=0, size=(800,600))
    # display.start()

    import os
    os.environ['DISPLAY'] = ':1'

    options = {
        'zoom': template_object.zoom,
        'format': 'jpg',
        'crop-h': str(template_object.crop_h),
        'crop-w': str(template_object.crop_w),
        'crop-x': str(template_object.crop_x),
        'crop-y': str(template_object.crop_y)
    }
    file_image = imgkit.from_string(
        html_content, False, options=options)
    encod_file = base64.b64encode(file_image).decode()
    img_cred = decode_base64_file(encod_file, full_credential_name)
    instance.credential_img = img_cred
    instance.save()
    user = instance.user
    user.credential_img = img_cred
    user.save()
    return instance.credential_img


def generate_certificate_image(user, domain):
    template_object = CredentialSettings.objects.last()
    template = Template(mark_safe(template_object.html_code))
    context = dict(
        names=user.names.upper(),
        STATIC_URL="%s/static/web" % domain)
    html_content = template.render(Context(context))

    import os
    os.environ['DISPLAY'] = ':1'

    options = {
        'zoom': template_object.zoom,
        'format': 'jpg',
        'crop-h': str(template_object.crop_h),
        'crop-w': str(template_object.crop_w),
        'crop-x': str(template_object.crop_x),
        'crop-y': str(template_object.crop_y)
    }
    file_image = imgkit.from_string(
        html_content, False, options=options)
    encod_file = base64.b64encode(file_image).decode()
    img_cert = decode_base64_file(encod_file, user.names)
    user.certificate_img = img_cert
    user.generated_certificate = True
    user.save()
    return user


def record_to_pdf(user, domain, company):
    settings = TicketSettings.objects.filter(company=company).last()
    ticket = user.user_tickets.filter(company=company).last()
    user_company = UserCompany.objects.get(company=company, user=user)
    filename = '%s.pdf' % ticket.code
    ticket_pdf = render_to_string(
        'landing/ticket.html',
        {'user': user_company,
         'domain': domain,
         'settings': settings,
         'ticket': ticket})
    print(ticket_pdf)
    html = HTML(string=ticket_pdf)
    css = CSS(string='@page { size: 350mm 150mm; margin: 4cm }')
    pdf = html.write_pdf(stylesheets=[css])
    file_data = File(BytesIO(pdf))
    ticket.pdf.save(filename, file_data)
    user.generated_ticket = True
    user.save()
    return user


def generate_certificate_pdf(user_company):
    # user_company = UserCompany.objects.get(company=company, user=user)
    company = user_company.company
    c_settings, created = CerficateSettings.objects.get_or_create(
        company=company)
    filename = '%s.pdf' % user_company.full_name
    certificate_pdf = render_to_string(
        'landing/certificate.html',
        {'user': user_company, 'c_settings': c_settings}
        )
    font_config = FontConfiguration()
    html = HTML(string=certificate_pdf)
    css = CSS(string='''
            @page { size: 859mm 500mm; margin: 1cm;}
            @font-face {
            font-family: "InterTight";
            src: url(https://testrealv.s3.amazonaws.com/media/realvirtual/free_images/InterTight-VariableFont_wght.ttf);
            }
              ''')
    pdf = html.write_pdf(stylesheets=[css], font_config=font_config)
    file_data = File(BytesIO(pdf))
    user_company.certificate.save(filename, file_data)
    user_company.save()
    return user_company


