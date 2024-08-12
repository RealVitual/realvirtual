from django.contrib import admin
from .models import (Video, Sponsor, CredentialCustomer,
                     CredentialSettings, UserAnswer, ChoiceQuestion,
                     Question, TicketSettings, ExternalEvent,
                     SurveryChoiceQuestion, SurveryQuestion,
                     UserSurveyAnswer, NetworkingOption,
                     UserNetworkingPreference, FreeImage)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('position', 'company')
    list_filter = ('company', )


@admin.register(ExternalEvent)
class ExternalEventAdmin(admin.ModelAdmin):
    list_display = ('position', 'name', 'company')
    list_filter = ('company', )


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    # list_editable = ('name', 'company')
    list_filter = ('company', )


@admin.register(CredentialCustomer)
class CredentialCustomerAdmin(admin.ModelAdmin):
    list_display = ('names', 'credential_img', 'created')


@admin.register(CredentialSettings)
class CredentialSettingsAdmin(admin.ModelAdmin):
    list_display = ('title_credential', 'company')
    list_filter = ('company', )


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    # list_editable = ('name', 'company')
    list_filter = ('company', )


class ChoiceQuestionTabular(admin.TabularInline):
    model = ChoiceQuestion
    list_display = ('user', 'company')
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company', )
    inlines = [ChoiceQuestionTabular]


@admin.register(TicketSettings)
class TicketSettingsAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'company')
    list_filter = ('company', )


class SurveyChoiceQuestionTabular(admin.TabularInline):
    model = SurveryChoiceQuestion
    list_display = ('user', 'company')
    extra = 0


@admin.register(SurveryQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company', )
    inlines = [SurveyChoiceQuestionTabular]


@admin.register(UserSurveyAnswer)
class UserSurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    list_filter = ('company', )


@admin.register(NetworkingOption)
class NetworkingOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company', )


@admin.register(UserNetworkingPreference)
class UserNetworkingPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'networking_option', 'company')
    list_filter = ('company', 'networking_option')


@admin.register(FreeImage)
class FreeImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
