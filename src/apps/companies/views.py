from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from src.utils.pagination import CustomPaginator
from .serializers import (
    CustomerListSerializer)
import xlwt
from .models import UserCompany


class AdminCustomerViewSet(ModelViewSet):
    queryset = UserCompany.objects.none()
    serializer_class = CustomerListSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('names', )
    ordering_fields = ('names',)
    ordering = ('-modified',)
    pagination_class = CustomPaginator
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        user_company = UserCompany.objects.filter(
            company=request.company, user=request.user, is_admin=True)
        if request.user.is_superuser or user_company:
            pass
        else:
            return HttpResponseForbidden()
        return super(
            AdminCustomerViewSet, self
        ).dispatch(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['get'],
        url_path='download-xlsx',
        url_name='download-xlsx-list')
    def download_xlsx_list(self, request, pk=None):
        queryset = UserCompany.objects.filter(
            company=request.company, is_admin=False)
        return self.download_xlsx(queryset)

    def download_xlsx(self, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('CUSTOMERS')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Nombre y Apellido', 'Email', 'País',
                   'Profesión', 'Empresa', 'Cargo', 'Tipo']
        row_index = 0
        # Header
        for column_index, value in enumerate(columns):
            ws.write(row_index, column_index, value, font_style)

        for column_index in range(0, len(columns)):
            ws.col(column_index).width = 2962*3

        font_style = xlwt.XFStyle()
        c = 0
        for idx, o in enumerate(queryset):
            c += 1
            row = ws.row(c)
            value = o.user.full_name
            row.write(0, value)
            value = o.user.email
            row.write(1, value)
            value = o.user.country.name if o.user.country else ""
            row.write(2, value)
            value = o.user.occupation
            row.write(3, value)
            row.write(4, o.user.job_company)
            row.write(5, o.user.company_position)
            if o.virtual:
                row.write(6, "Virtual")
            elif o.in_person:
                row.write(6, "Presencial")
            else:
                row.write(6, "-")
            # tz = pytz.timezone("America/Lima")
            # value = o.created.astimezone(tz).strftime(
            #     "%d/%m/%Y, %H:%M:%S")
            # row.write(8, value)
        wb.save(response)
        return response

    @action(
        detail=False,
        methods=['get'],
        url_path='download-files-xlsx',
        url_name='download-xlsx-files')
    def download_xlsx_files(self, request, pk=None):
        queryset = Customer.objects.exclude(profile_image="").order_by('names')
        return self.download_files_list(queryset)

    def download_files_list(self, queryset):
        import pytz
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('CUSTOMERS')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Nombre y Apellido', 'email', 'archivo']
        row_index = 0
        # Header
        for column_index, value in enumerate(columns):
            ws.write(row_index, column_index, value, font_style)

        for column_index in range(0, len(columns)):
            ws.col(column_index).width = 2962*3

        font_style = xlwt.XFStyle()
        c = 0
        for idx, o in enumerate(queryset):
            c += 1
            row = ws.row(c)
            value = o.email
            row.write(0, value)
            value = o.names
            row.write(1, value)
            value = o.profile_image.name.split('/')[-1]
            row.write(2, value)

        wb.save(response)
        return response
