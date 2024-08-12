from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as UA

from .forms import CustomerChangeForm, CustomerCreationForm
from .models import (
    Customer, )


@admin.register(Customer)
class CustomerAdmin(UA):

    add_form = CustomerCreationForm
    form = CustomerChangeForm
    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'uuid_hash')
        }),
        (_('Personal info'), {
            'fields': ('generated_credential', 'company', 'names', 'last_name',
                       'full_name', 'occupation', 'jon_company',
                       'company_position',
                       'age_range', 'country', 'speciality',
                       'allow_networking',
                       'virtual', 'in_person')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'is_confirmed', 'confirm_code', 'groups',
                       'user_permissions')
        }),
        (_('Creacion'), {
            'fields': ('last_login', 'date_joined')
        })
    )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'password1', 'password2'),
    }), )
    list_display = ('email', 'names', 'document', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'names')
    ordering = ('-modified', )
    # actions = [export_as_excel_action(), ]
