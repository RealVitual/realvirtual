from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_exempt
from django import forms
from .models import (
    Company, HomePage, ItemMainEvent, Header,
    Footer, EmailSettings, EmailTemplate,
    UserCompany, Font, Enterprise, JobCompany,
    Occupation)
from prettyjson import PrettyJSONWidget
from django.utils.safestring import mark_safe


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'enterprise')
    list_filter = ('enterprise', )
    search_fields = ('name', 'enterprise__name', 'domain')


class ItemMainEventTabular(admin.TabularInline):
    model = ItemMainEvent
    extra = 0


@admin.register(HomePage)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('company', )
    inlines = [ItemMainEventTabular]


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
