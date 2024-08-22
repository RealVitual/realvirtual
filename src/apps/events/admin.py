from django.contrib import admin
from .models import (
    Event, Exhibitor, Schedule, Category, Filter,
    ScheduleCustomerEvent, Room, Shift)
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
            fields['categories'].queryset = Category.objects.filter(
                company=obj.company).order_by('filter__name', 'name')
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


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, MPTTModelAdmin)
