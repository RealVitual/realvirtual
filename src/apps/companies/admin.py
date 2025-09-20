from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_exempt
from django import forms
from .models import (
    Company, HomePage, ItemMainEvent, Header,
    Footer, EmailSettings, EmailTemplate,
    UserCompany, Font, Enterprise, JobCompany,
    Occupation, TemplateVersion, ItemModule,
    IndicatorsMainEvent, FilterEmailDomain)
from prettyjson import PrettyJSONWidget
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import os


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'enterprise')
    list_filter = ('enterprise', )
    search_fields = ('name', 'enterprise__name', 'domain')
    readonly_fields = (
        'logo_preview', 'banner_preview', 'mobile_banner_preview',
        'image_banner_preview')

    def get_fieldsets(self, request, obj=None):
        fielsets_version = []
        if obj is None:
            return [
                (_('Version y formato'), {
                    'fields': ('version', )
                }),
                (_('Información Principal'), {
                    'fields': (
                        'enterprise', 'domain', 'name', 'logo', 'logo_preview',
                        'main_event_name'
                    )
                }),
            ]
        else:
            version_obj = obj.version
            version = 1
            if version_obj:
                version = version_obj.version
            fieldsets = [
            ]
        # efeff3
        if version == 1:
            fielsets_version = [
                (_('Version y formato'), {
                    'fields': ('version', 'font')
                }),
                (_('Información Principal'), {
                    'fields': (
                        'enterprise', 'domain', 'name', 'logo', 'logo_preview',
                        'main_event_name', 'contact_phone'
                    )
                }),
                (_('Colores'), {
                    'fields': (
                        'button_color', 'button_text_color',
                        'section_color',
                    )
                }),
                (_('Contador, Comunicado y Cierre de landing'), {
                    'fields': (
                        'use_counter', 'counter_datetime', 'counter_text',
                        'close_landing', 'close_banner',
                        'close_mobile_banner', 'warning_img'
                    )
                }),
                (_('Banner Principal'), {
                    'fields': (
                        'banner', 'banner_preview',
                        'mobile_banner', 'mobile_banner_preview',
                        'image_banner', 'image_banner_preview',
                        'video_file'
                    )
                }),
                (_('Confirmación de usuarios'), {
                    'fields': (
                        'confirm_user', 'message_confirm_user',
                        'enable_credentials', 'enable_preferences'
                    )
                }),
                (_('Filtros'), {
                    'fields': (
                        'use_filters', 'use_rooms', 'use_shifts', 'use_dates'
                    )
                }),
                (_('Cierre de registro'), {
                    'fields': (
                        'title_closed_in_person_register',
                        'message_closed_in_person_register'
                    )
                }),
                (_('Forma de Acceso'), {
                    'fields': (
                        'is_virtual',
                        'in_person',
                        'is_private',
                        'access_type',
                        'allow_virtual_access'
                    )
                }),
                (_('Capacidad'), {
                    'fields': (
                        'capacity',
                        'current_quantity'
                    )
                }),
                (_('Documentos para Políticas'), {
                    'fields': (
                        'privacy_policy',
                        'protection_data_policy',
                        'cookies_policy',
                        'terms_and_conditions'
                    )
                }),
                (_('Formulario'), {
                    'fields': (
                        'names',
                        'names_field_title',
                        'last_name',
                        'last_names_field_title',
                        'job_company',
                        'job_company_names_field_title',
                        'job_company_select',
                        'company_position',
                        'company_position_names_field_title',
                        'phone',
                        'country',
                        'country_names_field_title',
                        'occupation',
                        'occupation_select',
                        'occupation_names_field_title',
                        'email_names_field_title',
                        'confirm_email_names_field_title'
                    )
                }),
                (_('Codigos'), {
                    'fields': (
                        'code_header',
                        'code_body',
                        'linkedin_pixel'
                    )
                }),
            ]
        elif version == 2:
            fielsets_version = [
                (_('Version'), {
                    'fields': ('version', )
                }),
                (_('Información Principal'), {
                    'fields': (
                        'enterprise', 'domain', 'name', 'logo', 'logo_preview',
                        'main_event_name', 'contact_phone'
                    )
                }),
                (_('Contador, Comunicado y Cierre de landing'), {
                    'fields': (
                        'use_counter', 'counter_datetime', 'counter_text',
                        'close_landing', 'close_banner',
                        'close_mobile_banner', 'warning_img'
                    )
                }),
                (_('Confirmación de usuarios'), {
                    'fields': (
                        'confirm_user', 'message_confirm_user',
                        'enable_credentials', 'enable_preferences'
                    )
                }),
                (_('Filtros'), {
                    'fields': (
                        'use_filters', 'use_rooms', 'use_shifts', 'use_dates'
                    )
                }),
                (_('Cierre de registro'), {
                    'fields': (
                        'title_closed_in_person_register',
                        'message_closed_in_person_register'
                    )
                }),
                (_('Forma de Acceso'), {
                    'fields': (
                        'is_virtual',
                        'in_person',
                        'is_private',
                        'access_type',
                        'allow_virtual_access',
                        'is_private_with_confirmation'
                    )
                }),
                (_('Capacidad'), {
                    'fields': (
                        'capacity',
                        'current_quantity'
                    )
                }),
                (_('Documentos para Políticas'), {
                    'fields': (
                        'privacy_policy',
                        'protection_data_policy',
                        'cookies_policy',
                        'terms_and_conditions'
                    )
                }),
                (_('Formulario'), {
                    'fields': (
                        'names',
                        'names_field_title',
                        'last_name',
                        'last_names_field_title',
                        'job_company',
                        'job_company_names_field_title',
                        'job_company_select',
                        'company_position',
                        'company_position_names_field_title',
                        'phone',
                        'country',
                        'country_names_field_title',
                        'occupation',
                        'occupation_select',
                        'occupation_names_field_title',
                        'email_names_field_title',
                        'confirm_email_names_field_title'
                    )
                }),
                (_('Codigos'), {
                    'fields': (
                        'code_header',
                        'code_body',
                        'linkedin_pixel'
                    )
                }),
            ]
        elif version == 3:
            fielsets_version = [
                (_('Version'), {
                    'fields': ('version', )
                }),
                (_('Información Principal'), {
                    'fields': (
                        'enterprise', 'domain', 'name', 'logo', 'logo_preview',
                        'main_event_name', 'contact_phone'
                    )
                }),
                (_('Contador, Comunicado y Cierre de landing'), {
                    'fields': (
                        'use_counter', 'counter_datetime', 'counter_text',
                        'close_landing', 'close_banner',
                        'close_mobile_banner', 'warning_img'
                    )
                }),
                (_('Confirmación de usuarios'), {
                    'fields': (
                        'confirm_user', 'message_confirm_user',
                        'filter_domain_user', 'title_filter_user',
                        'message_filter_domain_user',
                        'message_filter_found_domain_user',
                        'enable_credentials', 'enable_preferences'
                    )
                }),
                (_('Confirmación asistencia Talleres'), {
                    'fields': (
                        'message_confirm_workshop',
                        'message_confirm_waiting_list_workshop'
                    )
                }),
                (_('Cierre de registro'), {
                    'fields': (
                        'title_closed_in_person_register',
                        'message_closed_in_person_register'
                    )
                }),
                (_('Forma de Acceso'), {
                    'fields': (
                        'is_virtual',
                        'in_person',
                        'is_private',
                        'access_type',
                        'allow_virtual_access'
                    )
                }),
                (_('Capacidad'), {
                    'fields': (
                        'capacity',
                        'current_quantity'
                    )
                }),
                (_('Documentos para Políticas'), {
                    'fields': (
                        'privacy_policy',
                        'protection_data_policy',
                        'cookies_policy',
                        'terms_and_conditions'
                    )
                }),
                (_('Formulario'), {
                    'fields': (
                        'names',
                        'names_field_title',
                        'last_name',
                        'last_names_field_title',
                        'job_company',
                        'job_company_names_field_title',
                        'job_company_select',
                        'company_position',
                        'company_position_names_field_title',
                        'phone',
                        'country',
                        'country_names_field_title',
                        'occupation',
                        'occupation_select',
                        'occupation_names_field_title',
                        'email_names_field_title',
                        'confirm_email_names_field_title',
                        'speciality',
                        'speciality_names_field_title',
                    )
                }),
                (_('Codigos'), {
                    'fields': (
                        'code_header',
                        'code_body',
                        'linkedin_pixel'
                    )
                }),
            ]
        for fieldset in fielsets_version:
            fieldsets.append(fieldset)
        return fieldsets

    def logo_preview(self, obj):
        IMAGE_FILE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        if obj.logo:
            name, extension = os.path.splitext(obj.logo.name)
            if extension.lower() in IMAGE_FILE_TYPES:
                return format_html(
                    '<img src="{}" width="100" height="auto" />',
                    obj.logo.url
                )
            else:
                return format_html(
                    '<a href="{}">{}</a>', obj.logo.url, obj.logo.name)
        return "No File"

    def banner_preview(self, obj):
        IMAGE_FILE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        if obj.banner:
            name, extension = os.path.splitext(obj.banner.name)
            if extension.lower() in IMAGE_FILE_TYPES:
                return format_html(
                    '<img src="{}" width="150" height="auto" />',
                    obj.banner.url
                )
            else:
                return format_html(
                    '<a href="{}">{}</a>', obj.banner.url, obj.banner.name)
        return "No File"

    def mobile_banner_preview(self, obj):
        IMAGE_FILE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        if obj.mobile_banner:
            name, extension = os.path.splitext(obj.mobile_banner.name)
            if extension.lower() in IMAGE_FILE_TYPES:
                return format_html(
                    '<img src="{}" width="150" height="auto" />',
                    obj.mobile_banner.url
                )
            else:
                return format_html(
                    '<a href="{}">{}</a>',
                    obj.mobile_banner.url,
                    obj.mobile_banner.name
                )
        return "No File"

    def image_banner_preview(self, obj):
        IMAGE_FILE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        if obj.image_banner:
            name, extension = os.path.splitext(obj.image_banner.name)
            if extension.lower() in IMAGE_FILE_TYPES:
                return format_html(
                    '<img src="{}" width="150" height="auto" />',
                    obj.image_banner.url
                )
            else:
                return format_html(
                    '<a href="{}">{}</a>',
                    obj.image_banner.url,
                    obj.image_banner.name
                )
        return "No File"


class ItemMainEventTabular(admin.TabularInline):
    model = ItemMainEvent
    extra = 0


class ItemModuleTabular(admin.TabularInline):
    model = ItemModule
    extra = 0


class IndicatorsMainEventTabular(admin.TabularInline):
    model = IndicatorsMainEvent
    extra = 0


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('company', )

    def get_inlines(self, request, obj=None):
        if obj:
            version_obj = obj.company.version
            version = 1
            if version_obj:
                version = version_obj.version
            if version == 1:
                return [ItemMainEventTabular, ]
            elif version == 2:
                return [IndicatorsMainEventTabular, ItemModuleTabular]
            elif version == 3:
                return []
        else:
            return []

    def get_fieldsets(self, request, obj=None):
        fielsets_version = []
        if obj is None:
            return [
                ("Seleccione la Compañía", {
                    "fields": ("company", ),
                    "description": "Debe seleccionar una compañía antes de continuar."
                }),
            ]
        else:
            version_obj = obj.company.version
            version = 1
            if version_obj:
                version = version_obj.version
            fieldsets = [
                ("Información principal", {
                    "fields": ("company", ),
                    "description":
                        f"Empresa seleccionada: {obj.company} (Versión {str(version)})"
                })
            ]

        if version == 1:
            fielsets_version = [
                (
                    "Sección Banner Inicial", {
                        "fields": (
                            'buttons_color',
                            'text_buttons_color',
                            'first_title',
                            'main_title',
                            'banner_link',
                            'banner',
                            'mobile_banner',
                            'image_banner',
                            'home_video_url',
                            'video_file',
                            'secondary_title',
                            'date_description',
                            'time_description',
                        ),
                        "description": "Campos disponibles para la versión 1."
                    }
                ),
                (
                    "Sección Detalle de evento", {
                        "fields": (
                            'main_event_title',
                            'main_event_description',
                            'main_event_image',
                            'main_event_video_url',
                        ),
                        "description": "Campos disponibles para la versión 1."
                    }
                ),
                (
                    "Sección Agenda y Programación", {
                        "fields": (
                            'schedule_section_name',
                            'schedule_section_title',
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Expositores", {
                        "fields": (
                            'exhibitors_section_name',
                            'exhibitors_section_title',
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Auspiciadores", {
                        "fields": (
                            'sponsors_section_name',
                            'sponsors_section_text'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Galería", {
                        "fields": (
                            'gallery_section_name',
                            'gallery_section_text'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Votación", {
                        "fields": (
                            'vote_section_name',
                            'vote_section_text'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Networking", {
                        "fields": (
                            'networking_section_name',
                            'networking_description_text'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Encuesta", {
                        "fields": (
                            'survey_section_name',
                            'survey_description_text'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                )
            ]
        elif version == 2:
            fielsets_version = [
                (
                    "Sección Banner Principal", {
                        "fields": (
                            'main_title',
                            'date_description',
                            'time_description',
                            'address_description',
                            'banner',
                            'mobile_banner',
                            'image_banner'
                        ),
                        "description": f"Campos disponibles para la versión {version}."
                    }
                ),
                (
                    "Sección Secundaria Banner", {
                        "fields": (
                            'banner_second_section',
                            'banner_second_section_image',
                            'banner_second_section_file'
                        ),
                        "description": f"Campos disponibles para la versión {version}."
                    }
                ),
                (
                    "Sección Detalle de evento", {
                        "fields": (
                            'main_event_title',
                            'main_event_sub_title',
                            'main_event_description',
                            'main_event_image',
                            'main_event_video_url'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Módulos", {
                        "fields": (
                            'module_section_name',
                            'module_section_title',
                            'module_section_text'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Agenda y Programación", {
                        "fields": (
                            'schedule_section_name',
                            'schedule_section_title'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Expositores", {
                        "fields": (
                            'exhibitors_section_name',
                            'exhibitors_section_title'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Blog", {
                        "fields": (
                            'blog_section_name',
                            'blog_section_title',
                            "blog_button_title"
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Auspiciadores", {
                        "fields": (
                            'sponsors_section_name',
                            'sponsors_section_text'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Final", {
                        "fields": (
                            'final_image',
                        ),
                    }
                )
            ]
        elif version == 3:
            fielsets_version = [
                (
                    "Sección Banner Principal", {
                        "fields": (
                            'main_title',
                            'banner_description',
                            'image_banner',
                            'banner_second_section_image',
                            'banner_footer_section_image'
                        ),
                        "description": f"Campos disponibles para la versión {version}."
                    }
                ),
                (
                    "Sección Agenda y Programación", {
                        "fields": (
                            'schedule_section_name',
                            'schedule_section_title'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Expositores", {
                        "fields": (
                            'exhibitors_section_name',
                            'exhibitors_section_title'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Talleres", {
                        "fields": (
                            'workshop_section_name',
                            'workshop_section_image',
                            'workshop_section_url'
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Preguntas Frecuentes", {
                        "fields": (
                            'frequently_questions_section_name',
                        ),
                        "description": "Recuerde activar esta sección en configuración Header."
                    }
                ),
                (
                    "Sección Final", {
                        "fields": (
                            'final_image',
                        ),
                    }
                )
            ]
        for fieldset in fielsets_version:
            fieldsets.append(fieldset)
        return fieldsets


@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ('email', 'company', 'created')
    list_filter = ('company', 'company__enterprise')
    search_fields = ('email', 'company__name')


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ('company', )
    list_filter = ('company__enterprise', )
    search_fields = ('company__name', )

    def get_fieldsets(self, request, obj=None):
        fielsets_version = []
        if obj is None:
            return [
                ("Seleccione la Compañía", {
                    "fields": ("company", ),
                    "description": "Debe seleccionar una compañía antes de continuar."
                }),
            ]
        else:
            version_obj = obj.company.version
            version = 1
            if version_obj:
                version = version_obj.version
            fieldsets = [
                ("Información principal", {
                    "fields": ("company", ),
                    "description":
                        f"Empresa seleccionada: {obj.company} (Versión {str(version)})"
                })
            ]

        if version == 1:
            fielsets_version = [
                (
                    "Colores", {
                        "fields": (
                            'header_color',
                            'header_text_color',
                            'button_color',
                            'button_text_color'
                        ),
                    }
                ),
                (
                    "Formulario", {
                        "fields": (
                            'register_title',
                            'register_form_title',
                            'register_form_text',
                            'login_title'
                        ),
                    }
                ),
                (
                    "Acerca de", {
                        "fields": (
                            'show_about_section',
                            'about_section_header_name',
                        ),
                    }
                ),
                (
                    "Agenda", {
                        "fields": (
                            'schecule_header_name',
                            'show_schedule_section',
                        ),
                    }
                ),
                (
                    "Galería", {
                        "fields": (
                            'show_gallery_section',
                            'gallery_header_name'
                        ),
                    }
                ),
                (
                    "Votación", {
                        "fields": (
                            'show_vote_section',
                            'vote_header_name'
                        ),
                    }
                ),
                (
                    "Auspiciadores", {
                        "fields": (
                            'show_sponsors_section',
                            'sponsors_header_name'
                        ),
                    }
                ),
                (
                    "Networking", {
                        "fields": (
                            'show_networking_section',
                            'networking_header_name'
                        ),
                    }
                ),
                (
                    "Encuesta", {
                        "fields": (
                            'show_survey_section',
                            'survey_header_name'
                        ),
                    }
                ),
                (
                    "Más Eventos", {
                        "fields": (
                            'show_more_events',
                        ),
                    }
                ),
                (
                    "Expositores", {
                        "fields": (
                            'show_exhibitors_section',
                            'exhibitors_header_name'
                        ),
                    }
                ),
                (
                    "Contacto", {
                        "fields": (
                            'show_contact',
                            'contact_header_name'
                        ),
                    }
                ),
            ]
        elif version == 2:
            fielsets_version = [
                (
                    "Colores", {
                        "fields": (
                            'header_color',
                            'header_text_color',
                            'button_color',
                            'button_text_color'
                        ),
                    }
                ),
                (
                    "Formulario", {
                        "fields": (
                            'register_title',
                            'register_form_title',
                            'register_form_text',
                            'login_title'
                        ),
                    }
                ),
                (
                    "Acerca de", {
                        "fields": (
                            'show_about_section',
                            'about_section_header_name',
                        ),
                    }
                ),
                (
                    "Agenda", {
                        "fields": (
                            'schecule_header_name',
                            'show_schedule_section',
                        ),
                    }
                ),
                (
                    "Auspiciadores", {
                        "fields": (
                            'show_sponsors_section',
                            'sponsors_header_name'
                        ),
                    }
                ),
                (
                    "Expositores", {
                        "fields": (
                            'show_exhibitors_section',
                            'exhibitors_header_name'
                        ),
                    }
                ),
                (
                    "Blog", {
                        "fields": (
                            'show_blog_section',
                            'blog_header_name'
                        ),
                    }
                ),
            ]
        elif version == 3:
            fielsets_version = [
                (
                    "Colores", {
                        "fields": (
                            'header_color',
                            'header_text_color',
                            'button_color',
                            'button_text_color'
                        ),
                    }
                ),
                (
                    "Formulario", {
                        "fields": (
                            'register_title',
                            'register_form_title',
                            'register_form_text',
                            'login_title'
                        ),
                    }
                ),
                (
                    "Agenda", {
                        "fields": (
                            'schecule_header_name',
                            'show_schedule_section',
                        ),
                    }
                ),
                (
                    "Expositores", {
                        "fields": (
                            'show_exhibitors_section',
                            'exhibitors_header_name'
                        ),
                    }
                ),
                (
                    "Talleres", {
                        "fields": (
                            'show_workshops_section',
                            'workshops_header_name'
                        ),
                    }
                ),
                (
                    "Preguntas frecuentes", {
                        "fields": (
                            'show_frequently_questions_section',
                            'frequently_questions_header_name'
                        ),
                    }
                )
            ]
        for fieldset in fielsets_version:
            fieldsets.append(fieldset)
        return fieldsets


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('company', )
    list_filter = ('company__enterprise', )
    search_fields = ('company__name', )


@admin.register(JobCompany)
class JobCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', )
    list_filter = ('company', )
    search_fields = ('company__name', 'name')


@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', )
    list_filter = ('company', )
    search_fields = ('company__name', 'name')


admin.site.register(EmailSettings)
admin.site.register(TemplateVersion)
admin.site.register(Font)
admin.site.register(Enterprise)


class FixedPrettyJSONWidget(PrettyJSONWidget):
    class Media:
        js = ('admin/js/jquery.init.js', 'prettyjson/prettyjson.js',)
        css = {'all': ('prettyjson/prettyjson.css', )}


class EmailTemplateJsonForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        exclude = []
        widgets = {
            'contexto': FixedPrettyJSONWidget(attrs={'initial': 'parsed'}),
            'imagenes': FixedPrettyJSONWidget(attrs={'initial': 'parsed'}),
        }


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    form = EmailTemplateJsonForm
    # inlines = [MailingMediaTabular]
    # actions = [test_mail_templates]
    fields = (
        'company', 'email_type', 'name', 'from_email', 'from_name', 'subject',
        'html_code', 'html_preview')
    list_display = ('email_type', 'name', 'subject', 'company',
                    'is_active', 'from_email')
    search_fields = ('company__name', )
    list_filter = ('company__enterprise', 'company', 'email_type')
    readonly_fields = (
        'html_preview', )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.id is None:
            return self.readonly_fields
        # return tuple(self.readonly_fields) + ('code',)
        return tuple(self.readonly_fields)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def context_info(self, obj=None):
        import json
        context = dict()
        images = {}
        # print(images)
        context['imagenes'] = images
        # context_by_model(SiteSettings, context, key='site')
        # context_by_model(Customer, context, key='customer')
        # context['link'] = site.domain or 'https://fuzzpass.pe'
        context_field = '''
        <div class="jsonwidget" data-initial="parsed">
            <p>
                <button class="parseraw" type="button">Show parsed</button>
                <button class="parsed" type="button">Collapse all</button>
                <button class="parsed" type="button">Expand all</button>
            </p>
            <textarea name="context_readonly" rows="50">\n{}</textarea>
            <div class="parsed"></div>
        </div>
        '''
        return mark_safe(context_field.format(
            json.dumps(context)
        ))
        # return context

    @xframe_options_exempt
    def html_preview(self, obj):
        from django.urls import reverse
        if obj.pk is None:
            return mark_safe(
                '<h1>La previsualización estará lista al guardar</h1>'
            )
        wrapper = '''
        <iframe
            src="{}"
            width="960px"
            height="750px"
            frameborder="0">
        </iframe>
        '''
        return mark_safe(wrapper.format(
            reverse('admin:mailing_template_preview', kwargs={'pk': obj.pk})
        ))

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        my_urls = [
            path(
                'preview/<int:pk>/',
                self.admin_site.admin_view(self.preview_view),
                name='mailing_template_preview'
            ),
        ]
        return my_urls + urls

    def preview_view(self, request, *args, **kwargs):
        from django.template.response import HttpResponse
        from django.template import Context, Template
        mailing = self.model.objects.get(id=kwargs.get('pk'))
        res = HttpResponse()
        template = Template(mailing.html_code)
        context = dict()
        html_content = template.render(Context(context))
        res.write(html_content)
        return res


@admin.register(FilterEmailDomain)
class FilterEmailDomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', )
    list_filter = ('company', )
    search_fields = ('company__name', 'name')
