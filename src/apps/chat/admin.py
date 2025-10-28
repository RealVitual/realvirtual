from django.contrib import admin
from .models import Chat, Message
# from .actions import export_as_excel_action


# @admin.register(Chat)
# class ChatAdmin(admin.ModelAdmin):
#     list_display = ('code', 'event')
#     search_fields = ('code', )
#     list_filter = ('event', )


# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('correo', 'names', 'content', 'chat', 'timestamp')
#     search_fields = ('email', 'content', 'names')
#     list_filter = ('chat', )
#     # actions = [export_as_excel_action(), ]

#     def correo(self, obj):
#         if obj.email:
#             return obj.email
#         return "invitado"
