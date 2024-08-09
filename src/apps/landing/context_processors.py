from django.conf import settings
from django.urls import resolve
from src.apps.conf.models import Country
from src.apps.events.models import Event
from src.apps.companies.models import Footer, Header
from django.urls import reverse
from datetime import datetime
import pytz


def main_info(request, **kwargs):
    current_url = resolve(request.path_info).url_name
    user_url = ""
    company_exists = hasattr(request, 'company')
    if company_exists:
        is_live = False
        now = datetime.now().replace(microsecond=0)
        now = now.astimezone(pytz.utc)
        events = Event.objects.filter(is_active=True,
                                      company=request.company)
        footer, f_created = Footer.objects.get_or_create(
            company=request.company)
        header_section, h_created = Header.objects.get_or_create(
            company=request.company)
        for event in events:
            start_date = event.start_datetime
            end_date = event.end_datetime
            if now >= start_date and end_date > now:
                is_live = True
                break
        user = request.user
        data = {
            'countries': Country.objects.all(),
            'STATIC_VERSION': settings.STATIC_VERSION,
            'current_url': current_url,
            "logged_user": user,
            "header_section": header_section,
            "footer": footer
        }
        if user.is_authenticated:
            if user.in_person:
                user_url = reverse(
                    'landing:select_preferences')
                if user.user_tickets.filter(company=request.company):
                    user_url = reverse(
                        'landing:ticket_view')
            else:
                user_url = reverse(
                    'landing:generate_credential')
                if user.credentials.filter(company=request.company):
                    cred = user.credentials.filter(
                        company=request.company).last()
                    user_url = reverse(
                        'landing:credential_generated',
                        kwargs=dict(uid=cred.code))
            data['user_url'] = user_url
            data['is_live'] = is_live
        return data
    return {
        'countries': Country.objects.all(),
        'STATIC_VERSION': settings.STATIC_VERSION,
        'current_url': current_url
    }
