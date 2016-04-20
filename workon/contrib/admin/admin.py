import copy, os
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django.forms import ModelForm, NumberInput
from django.contrib import admin
from django.db import models
from .widgets import WorkonSplitDateTimeWidget

from django.contrib.admin import ModelAdmin as BaseModelAdmin, actions
from django.contrib.admin.sites import site as base_site, AdminSite as BaseAdminSite

from .menu import get_menu, Menu

class AdminSite(BaseAdminSite):

    login_form = None
    index_template = "admin/index.html"
    app_index_template = None
    login_template = None
    logout_template = None
    password_change_template = None
    password_change_done_template = None

    def __init__(self, *args, **kwargs):
        super(AdminSite, self).__init__(*args, **kwargs)
        self._registry = copy.copy(base_site._registry)

        root_path = os.path.abspath(os.path.dirname(__file__))

        settings.TEMPLATE_DIRS += (
            os.path.join(root_path, 'templates') + '/',
        )
        settings.TEMPLATES[0]['DIRS'] += (
            os.path.join(root_path, 'templates') + '/',
        )

        settings.STATICFILES_DIRS += (
            os.path.join(root_path, 'static') + '/',
        )

        BaseModelAdmin.change_list_template = "admin/change_list.html"

    def register(self, *args, **kwargs):
        if not kwargs.get('admin_class', None) or kwargs.get('admin_class') == BaseModelAdmin:
            kwargs['admin_class'] = ModelAdmin

        print kwargs
        return super(AdminSite, self).register(*args, **kwargs)

    def get_app_list(self, *args, **kwargs):

        return super(AdminSite, self).get_app_list(*args, **kwargs)

        # app_dict = self._build_app_dict(request)
        # app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        # menu = Menu({}, request, app_list).get_app_list()
        # # app_dict =

        # workon_menu = settings.WORKON.get('ADMIN').get('MENU')

        # # print workon_menu


        # # Sort the apps alphabetically.

        # new_app_list = []

        # for app in app_list:
        #     label = app.get('name')
        #     model = "%s.%s" % (app.get('app_label'), app.get('object_name'))
        #     print app, label, model


        # # Sort the models alphabetically within each app.
        # for app in app_list:
        #     app['models'].sort(key=lambda x: x['name'])


    #     return menu
    # @property
    # def urls(self):
    #     return self.get_urls(), 'admin', 'admin'


    # def get_urls(self):
    #     from django.conf.urls import url, include
    #     urls = super(BaseAdminSite, self).get_url()
    #     return [
    #         url(r'^', include(urls, namespace="admin"))
    #     ]

class ModelAdmin(BaseModelAdmin):
    change_list_template = "workon/admin/list/list.html"


class SortableModelAdminBase(object):
    """
    Base class for SortableTabularInline and SortableModelAdmin
    """
    sortable = 'order'

    class Media:
        js = ('workon/admin/js/sortables.js',)


class SortableListForm(ModelForm):
    """
    Just Meta holder class
    """
    class Meta:
        widgets = {
            'order': NumberInput(
                attrs={'class': 'hide input-mini workon-admin-sortable'})
        }


class SortableChangeList(ChangeList):
    """
    Class that forces ordering by sortable param only
    """

    def get_ordering(self, request, queryset):
        return [self.model_admin.sortable, '-' + self.model._meta.pk.name]


class SortableTabularInlineBase(SortableModelAdminBase):
    """
    Sortable tabular inline
    """

    def __init__(self, *args, **kwargs):
        super(SortableTabularInlineBase, self).__init__(*args, **kwargs)

        self.ordering = (self.sortable,)
        self.fields = self.fields or []
        if self.fields and self.sortable not in self.fields:
            self.fields = list(self.fields) + [self.sortable]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == self.sortable:
            kwargs['widget'] = SortableListForm.Meta.widgets['order']
        return super(SortableTabularInlineBase, self).formfield_for_dbfield(
            db_field, **kwargs)


class SortableTabularInline(SortableTabularInlineBase, admin.TabularInline):
    pass


class SortableGenericTabularInline(SortableTabularInlineBase,
                                   GenericTabularInline):
    pass


class SortableStackedInlineBase(SortableModelAdminBase):
    """
    Sortable stacked inline
    """
    def __init__(self, *args, **kwargs):
        super(SortableStackedInlineBase, self).__init__(*args, **kwargs)
        self.ordering = (self.sortable,)

    def get_fieldsets(self, *args, **kwargs):
        """
        Iterate all fieldsets and make sure sortable is in the first fieldset
        Remove sortable from every other fieldset, if by some reason someone
        has added it
        """
        fieldsets = super(SortableStackedInlineBase, self).get_fieldsets(
            *args, **kwargs)

        sortable_added = False
        for fieldset in fieldsets:
            for line in fieldset:
                if not line or not isinstance(line, dict):
                    continue

                fields = line.get('fields')
                if self.sortable in fields:
                    fields.remove(self.sortable)

                # Add sortable field always as first
                if not sortable_added:
                    fields.insert(0, self.sortable)
                    sortable_added = True
                    break

        return fieldsets

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == self.sortable:
            kwargs['widget'] = copy.deepcopy(
                SortableListForm.Meta.widgets['order'])
            kwargs['widget'].attrs['class'] += ' workon-admin-sortable-stacked'
            kwargs['widget'].attrs['rowclass'] = ' workon-admin-sortable-stacked-row'
        return super(SortableStackedInlineBase, self).formfield_for_dbfield(
            db_field, **kwargs)


class SortableStackedInline(SortableStackedInlineBase, admin.StackedInline):
    pass


class SortableGenericStackedInline(SortableStackedInlineBase,
                                   GenericStackedInline):
    pass


class SortableModelAdmin(SortableModelAdminBase, ModelAdmin):
    """
    Sortable tabular inline
    """
    list_per_page = 500

    def __init__(self, *args, **kwargs):
        super(SortableModelAdmin, self).__init__(*args, **kwargs)

        self.ordering = (self.sortable,)
        if self.list_display and self.sortable not in self.list_display:
            self.list_display = list(self.list_display) + [self.sortable]

        self.list_editable = self.list_editable or []
        if self.sortable not in self.list_editable:
            self.list_editable = list(self.list_editable) + [self.sortable]

        self.exclude = self.exclude or []
        if self.sortable not in self.exclude:
            self.exclude = list(self.exclude) + [self.sortable]

    def merge_form_meta(self, form):
        """
        Prepare Meta class with order field widget
        """
        if not getattr(form, 'Meta', None):
            form.Meta = SortableListForm.Meta
        if not getattr(form.Meta, 'widgets', None):
            form.Meta.widgets = {}
        form.Meta.widgets[self.sortable] = SortableListForm.Meta.widgets[
            'order']

    def get_changelist_form(self, request, **kwargs):
        form = super(SortableModelAdmin, self).get_changelist_form(request,
                                                                   **kwargs)
        self.merge_form_meta(form)
        return form

    def get_changelist(self, request, **kwargs):
        return SortableChangeList

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            max_order = obj.__class__.objects.aggregate(
                models.Max(self.sortable))
            try:
                next_order = max_order['%s__max' % self.sortable] + 1
            except TypeError:
                next_order = 1
            setattr(obj, self.sortable, next_order)
        super(SortableModelAdmin, self).save_model(request, obj, form, change)


# Quite aggressive detection and intrusion into Django CMS
# Didn't found any other solutions though
if 'cms' in settings.INSTALLED_APPS:
    try:
        from cms.admin.forms import PageForm

        PageForm.Meta.widgets = {
            'publication_date': WorkonSplitDateTimeWidget,
            'publication_end_date': WorkonSplitDateTimeWidget,
        }
    except ImportError:
        pass
