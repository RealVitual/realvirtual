from django.conf import settings
from django.urls import resolve
from django.utils.html import format_html
from src.apps.conf.models import Country
from django.urls import reverse


def main_info(request, **kwargs):
    current_url = resolve(request.path_info).url_name
    user = None
    user_url = ""
    if request.user.is_authenticated:
        user = request.user
        if user.in_person:
            user_url = "select_preferences"
            if user.user_tickets.filter(company=request.company):
                user_url = "ticket"
        else:
            user_url = "generate_credential"
            if user.credentials.filter(company=request.company):
                cred = user.credentials.filter(company=request.company).last()
                user_url = reverse(
                    'landing:credential_generated',
                    kwargs=dict(uid=cred.code))
    return {
        'countries': Country.objects.all(),
        'STATIC_VERSION': settings.STATIC_VERSION,
        'current_url': current_url,
        "user": user,
        "user_url": user_url
    }
