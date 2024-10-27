from django.conf import settings
from django.urls import resolve
from src.apps.conf.models import Country
from src.apps.events.models import Event, ScheduleCustomerEvent
from src.apps.companies.models import Footer, Header
from django.urls import reverse
from datetime import datetime
import pytz
from django.conf import settings
from src.apps.companies.models import UserCompany, JobCompany, Occupation


def main_info(request, **kwargs):
    current_url = resolve(request.path_info).url_name
    company_exists = hasattr(request, 'company')
    if company_exists:
        company = request.company
        is_live = False
        now = datetime.now().replace(microsecond=0)
        now = now.astimezone(pytz.utc)
        events = Event.objects.filter(is_active=True,
                                      company=company)
        footer, f_created = Footer.objects.get_or_create(
            company=company)
        header_section, h_created = Header.objects.get_or_create(
            company=company)
        for event in events:
            start_date = event.start_datetime
            end_date = event.end_datetime
            if now >= start_date and end_date > now:
                is_live = event
                break
        choose_access_type = False
        allow_register =  True
        if company.access_type == "HYBRID" and company.capacity > company.current_quantity:
            choose_access_type = True
        if company.capacity <= company.current_quantity:
            allow_register = False
        user = request.user
        data = {
            'STATIC_VERSION': settings.STATIC_VERSION,
            'current_url': current_url,
            "header_section": header_section,
            "footer": footer,
            'user_schedules_quantity': 0,
            'user_schedules': [],
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
            'choose_access_type': choose_access_type,
            'allow_register': allow_register,
            'company': company,
            'countries': Country.objects.all(),
            'job_companies': JobCompany.objects.filter(company=company),
            'occupations': Occupation.objects.filter(company=company)
        }
        if user.is_authenticated:
            ticket_url = ""
            credential_url = ""
            company_user = None
            if (UserCompany.objects.filter(user=user, company=company)):
                company_user = UserCompany.objects.get(
                    user=user, company=company)
                if company_user.in_person:
                    ticket_url = reverse(
                        'landing:select_preferences')
                    if user.user_tickets.filter(company=company):
                        ticket_url = reverse(
                            'landing:ticket_view')
                credential_url = ""
                if company.enable_credentials:
                    credential_url = reverse(
                        'landing:generate_credential')
                    if user.credentials.filter(company=company):
                        cred = user.credentials.filter(
                            company=company).last()
                        credential_url = reverse(
                            'landing:credential_generated',
                            kwargs=dict(uid=cred.code))
            user_schedules = ScheduleCustomerEvent.objects.filter(
                company=company, company_user=company_user).values_list(
                    'schedule__id', flat=True)
            data['ticket_url'] = ticket_url
            data['credential_url'] = credential_url
            data['is_live'] = is_live
            data['logged_user'] = user
            data['user_schedules'] = list(user_schedules)
            data['user_schedules_quantity'] = len(user_schedules)
            data['company_user'] = company_user
        return data
    return {
        'STATIC_VERSION': settings.STATIC_VERSION,
        'current_url': current_url,
        'user_schedules_quantity': 0,
        'user_schedules': []
    }
