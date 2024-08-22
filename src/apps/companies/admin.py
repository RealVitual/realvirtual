from django.contrib import admin
from .models import Company, HomePage, ItemMainEvent, Header, Footer


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')


class ItemMainEventTabular(admin.TabularInline):
    model = ItemMainEvent
    extra = 0


@admin.register(HomePage)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('company', )
    inlines = [ItemMainEventTabular]


admin.site.register(Header)
admin.site.register(Footer)
