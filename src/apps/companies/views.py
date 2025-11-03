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
from src.apps.landing.models import UserAnswer, VoteUserAnswer
from src.apps.events.models import (
    CustomerEvent, ScheduleCustomerWorkshop,
    ScheduleCustomerEvent
)
from django.conf import settings
from datetime import datetime


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
        return self.download_preferences_xlsx(user_answers, request.company)

    @action(
        detail=False,
        methods=['get'],
        url_path='download-workshop_customers',
        url_name='download-workshop_customers-list')
    def download_workshop_customers_list(self, request, pk=None):
        workshops = request.company.company_workshops.filter(
            is_active=True)
        queryset = ScheduleCustomerWorkshop.objects.filter(
            workshop__in=workshops).order_by('-created')
        return self.download_workshop_customers_xlsx(queryset)

    @action(
        detail=False,
        methods=['get'],
        url_path='download-scheduled-events',
        url_name='download-scheduled-events-list')
    def download_scheduled_events_list(self, request, pk=None):
        queryset = ScheduleCustomerEvent.objects.filter(
            company=request.company).order_by('-created')
        return self.download_scheduled_events_xlsx(queryset)

    @action(
        detail=False,
        methods=['get'],
        url_path='download-votes',
        url_name='download-votes-list')
    def download_votes_list(self, request, pk=None):
        queryset = VoteUserAnswer.objects.filter(
            company=request.company).order_by('-created')
        return self.download_votes_xlsx(queryset)

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
            if o.virtual and o.in_person:
                row.write(6, "Presencial")
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

    def download_preferences_xlsx(self, queryset, company):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="preferencias_{company.name}.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('preferencias')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [
            'Email', 'Nombre y Apellido',
            'Pregunta', 'Respuesta', 'Tipo', 'Creado'
        ]
        row_index = 0
        # Header
        for column_index, value in enumerate(columns):
            ws.write(row_index, column_index, value, font_style)

        for column_index in range(0, len(columns)):
            ws.col(column_index).width = 2962*3

        font_style = xlwt.XFStyle()
        c = 0
        for idx, o in enumerate(queryset):
            c_user = o.user.user_companies.filter(company=company).last()
            if c_user:
                c += 1
                row = ws.row(c)
                row.write(0, c_user.email)
                row.write(1, c_user.full_name)
                row.write(2, o.question.name)
                if o.question.open_question:
                    row.write(3, o.open_answer)
                    row.write(4, "Abierta")
                else:
                    row.write(3, o.choice_question.name)
                    row.write(4, "Cerrada")
                tz = pytz.timezone("America/Lima")
                value = o.created.astimezone(tz).strftime(
                    "%d/%m/%Y, %H:%M:%S")
                row.write(5, value)
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

    def download_workshop_customers_xlsx(self, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="workshop_customers.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('INSCRIPCIONES A TALLERES')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Taller', 'Email', 'Nombres y Apellidos', 'Tipo', 'fecha']
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
            value = '{} - {}'.format(o.workshop.title, o.workshop.name)
            row.write(0, value)
            value = o.company_user.email
            row.write(1, value)
            value = o.company_user.full_name
            row.write(2, value)
            value = "Inscrito" if o.confirmed else "Lista de espera"
            row.write(3, value)
            tz = pytz.timezone("America/Lima")
            value = o.created.astimezone(tz).strftime(
                "%d/%m/%Y, %H:%M:%S")
            row.write(4, value)
        wb.save(response)
        return response

    def download_scheduled_events_xlsx(self, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="scheduled_events_customers.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('AGENDADOS')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Email', 'Nombres y Apellidos', 'Horario', 'Fecha y Hora', 'Evento', 'Landing' , 'creado']
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
            value = o.schedule.name
            row.write(2, value)
            start_date = o.event.start_datetime.astimezone(
                pytz.timezone(settings.TIME_ZONE)).date()
            end_date = o.event.end_datetime.astimezone(
                pytz.timezone(settings.TIME_ZONE)).date()
            start_time = o.schedule.start_time
            end_time = o.schedule.end_time
            start_datetime = datetime.combine(
                start_date, start_time).astimezone(
                    pytz.timezone(settings.TIME_ZONE))
            end_datetime = datetime.combine(
                end_date, end_time).astimezone(
                    pytz.timezone(settings.TIME_ZONE))
            start_datetime_str = start_datetime.strftime(
                "%d/%m/%Y, %H:%M:%S")
            end_datetime_str = end_datetime.strftime(
                "%d/%m/%Y, %H:%M:%S")
            value = f"{start_datetime_str} - {end_datetime_str}"
            row.write(3, value)
            value = o.event.name
            row.write(4, value)
            value = o.company.name
            row.write(5, value)
            tz = pytz.timezone("America/Lima")
            value = o.created.astimezone(tz).strftime(
                "%d/%m/%Y, %H:%M:%S")
            row.write(6, value)
        wb.save(response)
        return response

    def download_votes_xlsx(self, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{self.request.company.name}_votes_customers.xls"'  # noqa

        wb = xlwt.Workbook(encoding='utf-8')

        # Sheet for attributes
        ws = wb.add_sheet('VOTOS')
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Email', 'Nombres y Apellidos', 'Empresa', 'Grupo de Votación', 'Pregunta', 'Respuesta', 'Fecha de Votación']
        row_index = 0
        # Header
        for column_index, value in enumerate(columns):
            ws.write(row_index, column_index, value, font_style)

        for column_index in range(0, len(columns)):
            ws.col(column_index).width = 2962*3

        font_style = xlwt.XFStyle()
        c = 0
        for idx, o in enumerate(queryset):
            cu = UserCompany.objects.get(company=o.company, email=o.user.email)
            c += 1
            row = ws.row(c)
            value = cu.email
            row.write(0, value)
            value = cu.full_name
            row.write(1, value)
            value = cu.job_company_select.name
            row.write(2, value)
            value = o.vote_category.name
            row.write(3, value)
            value = o.question.name
            row.write(4, value)
            value = o.choice_question.name
            row.write(5, value)
            tz = pytz.timezone("America/Lima")
            value = o.created.astimezone(tz).strftime(
                "%d/%m/%Y, %H:%M:%S")
            row.write(6, value)
        wb.save(response)
        return response
