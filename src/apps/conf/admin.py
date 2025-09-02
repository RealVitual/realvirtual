from django.contrib import admin
from .models import Country, Speciality


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'name', 'position')
    list_editable = ('name', 'position')

    def nombre(self, obj):
        return obj.name


admin.site.register(Speciality)
