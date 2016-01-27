import email as original_email
from django.apps import AppConfig
from django import get_version

from django.conf import settings
from django.contrib.admin import options
from django.contrib.admin.options import ModelAdmin
from django.db import models
from django import forms
from .modules.admin import widgets

class WorkonConfig(AppConfig):


    WORKON_ADMIN_FORM_SIZE_FULL = 'col-xs-12 col-sm-2:col-xs-12 col-sm-10'
    WORKON_ADMIN_FORM_SIZE_HALF = 'col-xs-12 col-sm-2:col-xs-12 col-sm-8 col-md-6 ' \
                          'col-lg-4'

    name = 'workon'
    verbose_name = u"Extensions"
    menu_position = 'vertical'
    django_version = get_version()
    list_per_page = 18
    list_filters_position = 'center'
    if hasattr(settings, 'PROJECT_NAME'):
        admin_name = '%s Admin' % getattr(settings, 'PROJECT_NAME')
    elif hasattr(settings, 'APP_NAME'):
        admin_name = '%s Admin' % getattr(settings, 'APP_NAME').capitalize()
    elif hasattr(settings, 'BASE_DIR'):
        admin_name = '%s Admin' % getattr(settings, 'BASE_DIR').capitalize()
    else:
        admin_name = 'Workon Admin'

    header_date_format = 'l, jS F Y'
    header_time_format = 'H:i'

    # form
    show_required_asterisk = True
    confirm_unsaved_changes = True

    form_size = WORKON_ADMIN_FORM_SIZE_HALF

    menu = getattr(settings, 'WORKON_ADMIN_CONFIG', {}).get('MENU')
    theme = getattr(settings, 'WORKON_ADMIN_CONFIG', {}).get('THEME', 'blue')

    # menu
    search_url = '/admin/auth/user/'
    menu_open_first_child = True


    def __init__(self, app_name, app_module):

        widgets.add_bs3_markup()
        self.override_widgets()
        self.setup_model_admin()

        if 'filer' in settings.INSTALLED_APPS:
            try:
                self.setup_filer_app()
            except Exception:
                pass

        super(WorkonConfig, self).__init__(app_name, app_module)


    def ready(self):
        from . import models
        super(WorkonConfig, self).ready()

        if 'django.contrib.auth' in settings.INSTALLED_APPS:
            self.setup_auth_app()

    def override_widgets(self):
        options.FORMFIELD_FOR_DBFIELD_DEFAULTS[models.DateField].update({
            'widget': widgets.CargoDateWidget
        })
        options.FORMFIELD_FOR_DBFIELD_DEFAULTS[models.DateTimeField].update({
            'form_class': forms.DateTimeField,
            'widget': widgets.CargoDateTimeWidget
        })

    def setup_model_admin(self):
        """
        Override some ModelAdmin defaults
        """
        ModelAdmin.actions_on_top = False
        ModelAdmin.actions_on_bottom = True
        ModelAdmin.list_per_page = self.list_per_page

    def setup_filer_app(self):
        """
        Override filer app defaults
        """
        from .admin.widgets import AutosizedTextarea
        from filer.admin.imageadmin import ImageAdminForm
        from filer.admin.fileadmin import FileAdminChangeFrom
        # from filer.admin import FolderAdmin

        def ensure_meta_widgets(meta_cls):
            if not hasattr(meta_cls, 'widgets'):
                meta_cls.widgets = {}
            meta_cls.widgets['description'] = AutosizedTextarea

        ensure_meta_widgets(ImageAdminForm.Meta)
        ensure_meta_widgets(FileAdminChangeFrom.Meta)
        # FolderAdmin.actions_on_top = False
        # FolderAdmin.actions_on_bottom = True

    def setup_auth_app(self):
        from django.contrib.auth.admin import UserAdmin, GroupAdmin

        UserAdmin.workon_admin_form_size = WorkonConfig.WORKON_ADMIN_FORM_SIZE_FULL
        GroupAdmin.workon_admin_form_size = WorkonConfig.WORKON_ADMIN_FORM_SIZE_FULL