from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from src.utils.pagination import CustomPaginator
from .serializers import (
    CustomerListSerializer)
import xlwt
from .models import UserCompany
from src.apps.customers.models import Customer
import pytz
from src.apps.landing.models import UserAnswer
from itertools import groupby
from operator import itemgetter
from src.apps.events.models import CustomerEvent


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
            company=request.company, is_admin=False).order_by(
                '-created'
            )
        return self.download_xlsx(queryset)

    @action(
        detail=False,
        methods=['get'],
        url_path='download-asistants',
        url_name='download-asistants-list')
    def download_asistants_list(self, request, pk=None):
        queryset = CustomerEvent.objects.filter(
            company_user__company=request.company).order_by(
                '-created'
            )
        return self.download_asistants_xlsx(queryset)

    @action(
        detail=False,
        methods=['get'],
        url_path='download-preferences',
        url_name='download-preferences-list')
    def download_preferences_list(self, request, pk=None):
        questions = request.company.company_questions.filter(
            is_active=True).order_by('position')
        user_answers = UserAnswer.objects.filter(question__in=questions).order_by('question__position')
        return self.download_preferences_xlsx(user_answers, questions, request.company)


    def download_xlsx(self, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('CUSTOMERS')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Nombre y Apellido', 'Email', 'País',
                   'Profesión', 'Empresa', 'Cargo', 'Tipo', 'Telefono', 'Creado']
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
            value = o.full_name
            row.write(0, value)
            value = o.email
            row.write(1, value)
            value = o.country.name if o.country else ""
            row.write(2, value)
            if o.occupation_select:
                value = o.occupation_select.name
            else:
                value = o.occupation
            row.write(3, value)
            if o.job_company_select:
                row.write(4, o.job_company_select.name)
            else:
                row.write(4, o.job_company)
            row.write(5, o.company_position)
            if o.virtual and o.in_person and o.confirmed:
                row.write(6, "Virtual / Presencial")
            elif o.in_person and o.confirmed:
                row.write(6, "Presencial")
            elif o.virtual:
                row.write(6, "Virtual")
            else:
                row.write(6, "-")
            tz = pytz.timezone("America/Lima")
            row.write(7, o.phone)
            value = o.created.astimezone(tz).strftime(
                "%d/%m/%Y, %H:%M:%S")
            row.write(8, value)
        wb.save(response)
        return response

    def download_preferences_xlsx(self, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('CUSTOMERS')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Nombre y Apellido', 'Email', 'País',
                   'Profesión', 'Empresa', 'Cargo', 'Tipo', 'Telefono', 'Creado']
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
            value = o.full_name
            row.write(0, value)
            value = o.email
            row.write(1, value)
            value = o.country.name if o.country else ""
            row.write(2, value)
            if o.occupation_select:
                value = o.occupation_select.name
            else:
                value = o.occupation
            row.write(3, value)
            if o.job_company_select:
                row.write(4, o.job_company_select.name)
            else:
                row.write(4, o.job_company)
            row.write(5, o.company_position)
            if o.virtual and o.in_person and o.confirmed:
                row.write(6, "Virtual / Presencial")
            elif o.in_person and o.confirmed:
                row.write(6, "Presencial")
            elif o.virtual:
                row.write(6, "Virtual")
            else:
                row.write(6, "-")
            tz = pytz.timezone("America/Lima")
            row.write(7, o.phone)
            value = o.created.astimezone(tz).strftime(
                "%d/%m/%Y, %H:%M:%S")
            row.write(8, value)
        wb.save(response)
        return response

    @action(
        detail=False,
        methods=['get'],
        url_path='download-files-xlsx',
        url_name='download-xlsx-files')
    def download_xlsx_files(self, request, pk=None):
        queryset = Customer.objects.exclude(
            profile_image="").order_by('names')
        return self.download_files_list(queryset)

    def download_files_list(self, queryset):
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

    def download_asistants_xlsx(self, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="asistencias.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('Asistencias')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['email', 'nombre y apellido', 'evento', 'fecha de asistencia']

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
            value = o.company_user.email
            row.write(0, value)
            value = o.company_user.full_name
            row.write(1, value)
            value = o.event.name
            row.write(2, value)
            tz = pytz.timezone("America/Lima")
            value = o.created.astimezone(tz).strftime(
                "%d/%m/%Y, %H:%M:%S")
            row.write(3, value)
        wb.save(response)
        return response
