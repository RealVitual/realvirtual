from django.contrib import admin
from .models import (
    Event, Exhibitor, Schedule, Category, Filter,
    ScheduleCustomerEvent)
from mptt.admin import MPTTModelAdmin


class ScheduleTabular(admin.TabularInline):
    model = Schedule
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            fields = formset.form.base_fields
            fields['exhibitors'].queryset = Exhibitor.objects.filter(
                company=obj.company)
        return formset


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_datetime',  'company')
    inlines = [ScheduleTabular]
    list_editable = ('company', )
    list_filter = ('company', )

    def get_inline_instances(self, request, obj=None):
        if obj:
            return [ScheduleTabular(self.model, self.admin_site)]
        return []


@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_editable = ('company', )
    list_filter = ('company', )


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company', )


@admin.register(ScheduleCustomerEvent)
class ScheduleCustomerEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'event', 'schedule')
    list_filter = ('company', 'event', 'schedule')


admin.site.register(Category, MPTTModelAdmin)
