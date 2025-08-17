from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_exempt
from django import forms
from .models import (
    Company, HomePage, ItemMainEvent, Header,
    Footer, EmailSettings, EmailTemplate,
    UserCompany, Font, Enterprise, JobCompany,
    Occupation, TemplateVersion, ItemModule, IndicatorsMainEvent)
from prettyjson import PrettyJSONWidget
from django.utils.safestring import mark_safe


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'enterprise')
    list_filter = ('enterprise', )
    search_fields = ('name', 'enterprise__name', 'domain')
    fieldsets = (
        (None, {
            'fields': ('enterprise', 'domain', 'name', 'main_event_name')
        }),
        (_('Contador, Comunicado y Cierre de landing'), {
            'fields': (
                'use_counter', 'counter_datetime', 'counter_text',
                'close_landing', 'close_banner',
                'close_mobile_banner', 'warning_img'
            )
        }),
        (_('Version y formato'), {
            'fields': ('version', 'font')
        }),
        (_('Banner Principal'), {
            'fields': (
                'banner', 'mobile_banner', 'image_banner',
                'banner_second_section', 'banner_second_section_image',
                'banner_second_section_internal_title',
                'banner_second_section_internal_text',
                'banner_second_section_internal_image',
                'video_file'
            )
        }),
        (_('Confirmación de usuarios'), {
            'fields': (
                'confirm_user', 'message_confirm_user'
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
    )


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

    def get_fieldsets(self, request, obj=None):
        fielsets_version = []
        print(obj, 'OJB')
        if obj is None:
            return [(
                ("Seleccione la Compañía", {
                    "fields": ("company", ),
                    "description": "Debe seleccionar una compañía antes de continuar."
                }),
            )]
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
                            'banner_second_section_internal_title',
                            'banner_second_section_internal_text',
                            'banner_second_section_internal_image'
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
    list_display = ('name', 'subject', 'company',
                    'is_active', 'from_email')
    search_fields = ('company__name', )
    list_filter = ('company__enterprise', 'company')
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
