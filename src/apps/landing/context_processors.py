from django.conf import settings
from django.urls import resolve
from src.apps.conf.models import Country
from src.apps.events.models import Event
from django.urls import reverse
from datetime import datetime
import pytz


def main_info(request, **kwargs):
    current_url = resolve(request.path_info).url_name
    user_url = ""
    company_exists = hasattr(request, 'company')
    if request.user.is_authenticated and company_exists:
        is_live = False
        now = datetime.now().replace(microsecond=0)
        now = now.astimezone(pytz.utc)
        events = Event.objects.filter(is_active=True)
        for event in events:
            start_date = event.start_datetime
            end_date = event.end_datetime
            if now >= start_date and end_date > now:
                is_live = True
                break
        user = request.user
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
                cred = user.credentials.filter(company=request.company).last()
                user_url = reverse(
                    'landing:credential_generated',
                    kwargs=dict(uid=cred.code))
        return {
            'countries': Country.objects.all(),
            'STATIC_VERSION': settings.STATIC_VERSION,
            'current_url': current_url,
            "logged_user": user,
            "user_url": user_url,
            "is_live": is_live
        }
    return {
        'countries': Country.objects.all(),
        'STATIC_VERSION': settings.STATIC_VERSION,
        'current_url': current_url
    }
