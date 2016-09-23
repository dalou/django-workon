from .contrib.user.admin import UserAdmin
from .contrib.tree.admin import TreeAdmin
# from .contrib.google.admin import GoogleAPISettingsAdmin
from .contrib.unique.admin import UniqueAdmin
# from .contrib.stripe.admin import *
from .contrib.auth.admin import *
# # from .setting import SettingsAdmin

from django.conf import settings

if 'workon.contrib.admin' in settings.INSTALLED_APPS:

    from .contrib.admin.admin import *
    from django.contrib import admin


elif 'workon.contrib.admin2' in settings.INSTALLED_APPS:

    from .contrib.admin2.admin import *
    from django.contrib import admin2 as admin

class ViewableOnly(admin.ModelAdmin):

    actions = []

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them
    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super(ViewableOnly, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False