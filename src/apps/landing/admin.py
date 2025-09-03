from django.contrib import admin
from .models import (Video, Sponsor, CredentialCustomer,
                     CredentialSettings, UserAnswer, ChoiceQuestion,
                     Question, TicketSettings, ExternalEvent,
                     SurveryChoiceQuestion, SurveryQuestion,
                     UserSurveyAnswer, NetworkingOption,
                     UserNetworkingPreference, FreeImage, CerficateSettings,
                     BlogPost, BlogPostItem, BlogPostItemContent, FrequentlyQuestion,
                     CustomerInvitedLanding)
from django.utils.html import format_html
import os


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
    list_display = ('image_preview', 'position', 'company')
    list_editable = ('position', 'company')
    list_filter = ('company', )
    readonly_fields = ('image_preview', )

    fieldsets = (
        (None, {
            'fields': (
                'image_preview',
            )
        }),
        (None, {
            'fields': (
                'company', 'position', 'name', 'image',
            )
        }),
    )

    def image_preview(self, obj):
        IMAGE_FILE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        if obj.image:
            name, extension = os.path.splitext(obj.image.name)
            if extension.lower() in IMAGE_FILE_TYPES:
                return format_html(
                    '<img src="{}" width="100" height="auto" />',
                    obj.image.url
                )
            else:
                return format_html(
                    '<a href="{}">{}</a>', obj.image.url, obj.image.name)
        return "No File"


@admin.register(CredentialCustomer)
class CredentialCustomerAdmin(admin.ModelAdmin):
    list_display = ('names', 'credential_img', 'created')


@admin.register(CredentialSettings)
class CredentialSettingsAdmin(admin.ModelAdmin):
    list_display = ('company', )
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
    list_display = ('company', 'event_name', )
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


class BlogPostItemTabular(admin.TabularInline):
    model = BlogPostItem
    extra = 0


class BlogPostItemContentTabular(admin.TabularInline):
    model = BlogPostItemContent
    extra = 0


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active')
    list_filter = ('company', )
    list_editable = ('company', 'is_active')
    inlines = BlogPostItemContentTabular, BlogPostItemTabular


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
    list_display = ('user_company', 'networking_option', 'company')
    list_filter = ('company', 'networking_option')


@admin.register(FreeImage)
class FreeImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(FrequentlyQuestion)
class FrequentlyQuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company', )


admin.site.register(CerficateSettings)
admin.site.register(CustomerInvitedLanding)
