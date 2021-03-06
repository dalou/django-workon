import os

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django import get_version
from django.contrib.admin.options import ModelAdmin

from workon.utils import get_project_title


from django import forms
from . import widgets

class AdminConfig(AppConfig):
    name = 'workon.contrib.admin2'
    label = 'workon_admin2'
    verbose_name = _("Admin")

    list_per_page = 18
    list_filters_position = 'center'

    verbose_name = u"Extensions"
    menu_position = 'horizontal'

    header_date_format = 'l, jS F Y'
    header_time_format = 'H:i'

    show_required_asterisk = True
    confirm_unsaved_changes = True

    WORKON_ADMIN_FORM_SIZE_FULL = 'col-xs-12 col-sm-2:col-xs-12 col-sm-10'
    WORKON_ADMIN_FORM_SIZE_HALF = 'col-xs-12 col-sm-2:col-xs-12 col-sm-8 col-md-6 ' \
                          'col-lg-4'


    form_size = WORKON_ADMIN_FORM_SIZE_FULL
    menu_open_first_child = True

    def __init__(self, app_name, app_module):

        config = getattr(settings, 'WORKON', {}).get('ADMIN', None)
        if not config:
            config = getattr(settings, 'WORKON_ADMIN', {})


        self.admin_name = config.get('ADMIN_NAME', '%s Admin' % get_project_title())
        self.menu = config.get('MENU')
        self.layout = config.get('LAYOUT', 'vertical')
        self.theme = config.get('THEME', 'dark')
        self.VISUAL_LOCK = config.get('VISUAL_LOCK', True)

        self.version = config.get('VERSION', '2')
        if not self.version in ['1', '2', '3']:
            self.version = '2'

        self.search_url = config.get('SEARCH_URL', '/admin/auth/user/')

        super(AdminConfig, self).__init__(app_name, app_module)

    def ready(self):

        widgets.add_bs3_markup()

        ModelAdmin.actions_on_top = False
        ModelAdmin.actions_on_bottom = True
        ModelAdmin.list_per_page = self.list_per_page

        try:
            self.setup_filer_app()
        except Exception:
            pass

        self.contrib_dir = os.path.dirname(os.path.abspath(__file__))
        import django
        self.django_contrib_dir = os.path.join(os.path.dirname(os.path.abspath(django.__file__)), "contrib/admin")

        print self.django_contrib_dir
        print self.contrib_dir
        try:
            import shutil
            shutil.copy2(
                os.path.join(self.django_contrib_dir, 'templates','admin', 'base.html'),
                os.path.join(self.contrib_dir, 'templates','admin', 'base_django.html')
            )
        except Exception, e:
            print str(e.message)
        # try:
        #     os.unlink(os.path.join(self.contrib_dir, 'templates', 'registration'))
        # except Exception, e:
        #     print str(e.message)
        # try:
        #     os.symlink(
        #         os.path.join(self.contrib_dir, 'templates', 'admin_v%s' % self.version),
        #         os.path.join(self.contrib_dir, 'templates', 'admin')
        #     )
        # except Exception, e:
        #     print str(e.message)
        # try:
        #     os.symlink(
        #         os.path.join(self.contrib_dir, 'templates', 'registration_v%s' % self.version),
        #         os.path.join(self.contrib_dir, 'templates', 'registration')
        #     )
        # except Exception, e:
        #     print str(e.message)

        super(AdminConfig, self).ready()

        if 'django.contrib.auth' in settings.INSTALLED_APPS:
            self.setup_auth_app()

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

        UserAdmin.workon_admin_form_size = self.WORKON_ADMIN_FORM_SIZE_FULL
        GroupAdmin.workon_admin_form_size = self.WORKON_ADMIN_FORM_SIZE_FULL