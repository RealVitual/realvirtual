from django.contrib import admin
from .models import Ticket, TicketUse
# from .actions import export_as_excel_action


class TicketUseInline(admin.TabularInline):
    model = TicketUse
    fields = ('used_date', 'date_created')
    readonly_fields = ('date_created', )
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('code', 'company', 'user', 'created')
    search_fields = ('email', 'code', 'full_name')
    # actions = [export_as_excel_action(), ]
    inlines = [TicketUseInline, ]
    list_filter = ['company', 'status']
