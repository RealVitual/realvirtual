"""
    Core classes
"""
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param


class CustomPaginator(PageNumberPagination):
    """
    Custom Paginator
    """
    page_size_query_param = 'page_size'
    page_size = 25
    max_page_size = 100

    def get_paginated_response(self, data, return_data=False):
        page_size = self.request.GET.get('page_size', self.page_size)
        data_to_response = {
            'meta': {
                'pagination': {
                    'page_size': page_size,
                    'total_items': self.page.paginator.count,
                    'total_pages': self.page.paginator.num_pages,
                },
                'links': {
                    'first': 1,
                    'previous': self.get_previous_number(),
                    'current': self.page.number,
                    'next': self.get_next_number(),
                    'last': self.page.paginator.num_pages,
                }
            },
            'items': data,
        }
        if return_data:
            return data_to_response
        return Response(data_to_response)

    def build_link(self, index):
        if not index:
            return None
        url = self.request and self.request.build_absolute_uri() or ''
        return replace_query_param(url, self.page_query_param, index)

    def get_next_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return replace_query_param('', self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return replace_query_param('', self.page_query_param, page_number)


class CustomPaginatorCatalog(CustomPaginator):
    page_size = 24
