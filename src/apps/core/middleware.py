

import operator
from .utils import site_domain_list
from src.apps.companies.models import Company
from django.utils.deprecation import MiddlewareMixin
lower = operator.methodcaller('lower')
get_domain_list = site_domain_list


class MySubdomainMiddleware(MiddlewareMixin):
    def get_domains_for_request(self, request):
        return get_domain_list()

    def process_request(self, request):
        for domain in self.get_domains_for_request(request):
            domain, host = map(lower, (domain, request.get_host()))
            host = host.removeprefix('www.').split(':')[0]
            if domain == host:
                request.subdomain = domain
                try:
                    request.company = Company.objects.get(
                        domain=request.subdomain)
                except Company.DoesNotExist:
                    request.company = Company.objects.none()
                return
            else:
                request.subdomain = None
