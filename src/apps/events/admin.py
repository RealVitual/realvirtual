from django.contrib import admin
from .models import (
    Event, Exhibitor, Schedule, Category, Filter,
    ScheduleCustomerEvent, Room, Shift, CustomerEvent,
    Workshop, ScheduleCustomerWorkshop)
from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html
import os


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
    list_filter = ('company', 'company__enterprise')
    search_fields = ('name', 'company__name')

    def get_inline_instances(self, request, obj=None):
        if obj:
            return [ScheduleTabular(self.model, self.admin_site)]
        return []


@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'image_preview', 'company', 'is_active', 'position'
    )
    list_editable = ('company', 'is_active', 'position')
    list_filter = ('company', )
    search_fields = ('name', )
    readonly_fields = ('image_preview', )

    fieldsets = (
        ("Expositor", {
            'fields': (
                'company',   'name', 'title', 'name_on_list',
                'organization', 'image', 'image_preview', 'description',
                'flag_image'

            )
        }),
        ("Activación", {
            'fields': (
                'position',
                'is_active', 'is_principal', 'text_is_principal'
            )
        }),
        ("Link", {
            'fields': (
                'link', 'link_title',
            )
        }),
    )

    def image_preview(self, obj):
        IMAGE_FILE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        if obj.image:
            name, extension = os.path.splitext(obj.image.name)
            if extension.lower() in IMAGE_FILE_TYPES:
                return format_html(
                    f"""<a target="_blank" href="{obj.image.url}">
                    <img src="{obj.image.url}" width="100" height="auto" />
                    </a>""",
                )
            else:
                return format_html(
                    '<a href="{}">{}</a>', obj.image.url, obj.image.name)
        return "No File"


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company', )


@admin.register(ScheduleCustomerEvent)
class ScheduleCustomerEventAdmin(admin.ModelAdmin):
    list_display = ('company_user', 'company', 'event', 'schedule')
    list_filter = ('company', 'event', 'schedule')


@admin.register(CustomerEvent)
class CustomerEventAdmin(admin.ModelAdmin):
    list_display = ('company_user', 'event')
    list_filter = ('company_user__company', 'event')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduleCustomerWorkshop)
class ScheduleCustomerWorkshopAdmin(admin.ModelAdmin):
    list_display = ('company_user', 'company', 'workshop')
    list_filter = ('company',  'workshop')


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'name', 'image_preview', 'company', 'is_active', 'position'
    )
    list_editable = ('company', 'is_active', 'position')
    list_filter = ('company', )
    search_fields = ('name', )
    readonly_fields = ('image_preview', )

    def get_fieldsets(self, request, obj=None):
        fielsets_version = []
        if obj is None:
            return [
                ('Taller', {
                    "fields": (
                        'is_active', 'company', 'position', 'title', 'name',
                        'image', 'description',
                    ),
                }),
                ('Ubicación y fecha', {
                    "fields": (
                        'address', 'start_datetime', 'end_datetime',
                        'ics_file',
                    ),
                }),
                ('Capacidad', {
                    'fields': (
                        'capacity', 'enrolled',
                        'waiting_list_capacity', 'waiting_list_enrolled'
                    )
                })
            ]
        else:
            fieldsets = [
                ('Taller', {
                    'fields': (
                        'is_active', 'company', 'position', 'title', 'name',
                        'image', 'image_preview', 'description',
                    ),
                }),
                ('Ubicación y fecha', {
                    "fields": (
                        'address', 'start_datetime', 'end_datetime',
                        'ics_file',
                    ),
                }),
                ('Capacidad', {
                    'fields': (
                        'capacity', 'enrolled',
                        'waiting_list_capacity', 'waiting_list_enrolled'
                    )
                })
            ]
        for fieldset in fielsets_version:
            fieldsets.append(fieldset)
        return fieldsets

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "exhibitor":
            obj = self.get_object(
                request, request.resolver_match.kwargs.get('object_id'))
            if obj:
                kwargs["queryset"] = Exhibitor.objects.filter(
                    company=obj.company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def image_preview(self, obj):
        IMAGE_FILE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        if obj.image:
            name, extension = os.path.splitext(obj.image.name)
            if extension.lower() in IMAGE_FILE_TYPES:
                return format_html(
                    f"""<a target="_blank" href="{obj.image.url}">
                    <img src="{obj.image.url}" width="200" height="150" />
                    </a>""",
                )
            else:
                return format_html(
                    '<a href="{}">{}</a>', obj.image.url, obj.image.name)
        return "No File"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            fields = formset.form.base_fields
            fields['exhibitor'].queryset = Exhibitor.objects.filter(
                company=obj.company)
        return formset


admin.site.register(Category, MPTTModelAdmin)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'allow_schedule', 'ics_file',
                    'start_time', 'end_time', 'event')
    list_editable = ('allow_schedule', 'ics_file')
    list_filter = ('event', 'event__company')
    search_fields = ('name', 'event__name')
