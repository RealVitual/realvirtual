from django.conf import settings
from src.apps.companies.models import Company


def site_domain_list():
    domain_list = [company.domain for company in Company.objects.all()]

    prefix = 'www.'
    for domain in domain_list:
        if getattr(settings, 'REMOVE_WWW_FROM_DOMAIN', False) \
                and domain.startswith(prefix):
            domain_list[domain_list.index(domain)] = domain.replace(
                prefix, '', 1)
    return domain_list
