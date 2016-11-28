from django.contrib import admin

# from .models import Notification


# # class NotificationAdmin(admin.ModelAdmin):
# #     list_display = ('receiver', 'uid', 'subject', 'context_object', 'is_sent', 'is_read', 'is_email_sent')
# #     list_select_related = ( )

# #     readonly_fields = (
# #         'receiver', 'uid', 'subject', 'message', 'is_sent', 'is_read', 'is_email_sendable', 'is_email_sent', 'context_object_id', 'context_content_type',
# #     )

# #     def has_add_permission(self, obj):
# #         return False

# # admin.site.register(Notification, NotificationAdmin)