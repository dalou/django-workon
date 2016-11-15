# encoding: utf-8

from functools import update_wrapper
from django.conf import settings
from django.contrib import messages
from django.contrib import admin
from django import forms
from django.conf.urls import url
from django.db import models
from django import forms
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse


from .models import *


class SelectionAddForm(forms.ModelForm):
    selection = forms.ModelChoiceField(label=u"Ajouter à une sélection existante", queryset=Selection.objects.all(), required=True)
    class Meta:
        model = Selection
        fields = ('selection', 'ids')
    def __init__(self, *args, **kwargs):
        super(SelectionAddForm, self).__init__(*args, **kwargs)
        self.fields['ids'].widget.attrs['readonly'] = True
        self.fields['ids'].widget.attrs['style'] = "display:none"

class SelectionForm(forms.ModelForm):

    # new_selection = forms.TextField(label="")
    existing_selection = forms.ModelChoiceField(label=u"Écraser une sélection existante", queryset=Selection.objects.all(), required=False)

    class Meta:
        model = Selection
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        super(SelectionForm, self).__init__(*args, **kwargs)
        self.fields['ids'].widget.attrs['readonly'] = True
        # self.fields['user'].widget.attrs['readonly'] = True
        self.fields['content_type'].widget.attrs['readonly'] = True

        self.fields['ids'].widget.attrs['style'] = "display:none"
        # self.fields['user'].widget.attrs['style'] = "display:none"
        self.fields['content_type'].widget.attrs['style'] = "display:none"


class SelectionFilter(admin.SimpleListFilter):
    title = u"Charger une selection"
    parameter_name = 'selection_load'

    def lookups(self, request, model_admin):
        return sorted([ (str(selection.id), selection.name) for selection in Selection.objects.all() ], key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            selection = Selection.objects.get(id=self.value())
            ids = selection.get_ids()
            messages.success(request, u"Selection \"%s\" chargée avec succés" % selection.name )
            return queryset.filter(id__in=ids)
        return queryset

class SelectionAdmin(admin.ModelAdmin):

    selection_add_template_name = 'workon/selection/admin/add.html'
    selection_save_template_name = 'workon/selection/admin/save.html'

    def __init__(self, *args, **kwargs):
        super(SelectionAdmin, self).__init__(*args, **kwargs)
        if not 'action_selection_save' in self.actions:
            self.actions += ('action_selection_save',)
        if not 'action_selection_add' in self.actions:
            self.actions += ('action_selection_add',)
        if not SelectionForm in self.list_filter:
            self.list_filter += (SelectionFilter, )

    def get_urls(self):

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = super(SelectionAdmin, self).get_urls()

        def add_url(regex, url_name, view):
            # Prepend url to list so it has preference before 'change' url
            urlpatterns.insert(
                0,
                url(
                    regex,
                    wrap(view),
                    name='%s_%s_%s' % (
                        self.model._meta.app_label,
                        self.model.__class__.__name__,
                        url_name
                    )
                )
            )

        add_url(r'^selection/save/$', 'selection_save', self.selection_save)
        add_url(r'^selection/add/$', 'selection_add', self.selection_add)
        # add_url(r'^selection/load/$', 'selection_load', self.selection_load)
        return urlpatterns

    def get_admin_url(self, name, args=None):
        opts = self.model._meta
        url_name = 'admin:%s_%s_%s' % (opts.app_label, self.model.__class__.__name__, name)

        return reverse(
            url_name,
            args=args,
            current_app=self.admin_site.name
        )

    # def get_readonly_fields(self, *args, **kwargs):
    #     fields = [f.name for f in self.model._meta.fields]
    #     return fields

    def action_selection_add(self, request, queryset):
        ids = ",".join(map(str, queryset.values_list('id', flat=True)))
        content_type = ContentType.objects.get_for_model(queryset.model)
        form = SelectionAddForm(initial={
            'ids': ids,
            'content_type': content_type,
            # 'user': request.user
        })
        return render(request, self.selection_add_template_name,
        {
            'queryset': Selection.get_queryset_for_ids(content_type, ids),
            'selections': Selection.objects.all(),
            'form_url': self.get_admin_url('selection_add'),
            'queryset': queryset,
            'form': form
        })

    action_selection_add.short_description = u"Ajouter à la selection"



    def selection_add(self, request, force=False):
        if request.method == "POST":
            if request.POST.get('_selection_add') or force:
                form = SelectionAddForm(request.POST)
                if form.is_valid():
                    selection = form.cleaned_data.get('selection')
                    selection.ids += ","+form.cleaned_data.get('ids')
                    selection.save()

                    self.selection_id = selection.pk

                    messages.success(request, u"Selection \"%s\" enregistrée avec succés" % selection.name )
                else:
                    content_type = ContentType.objects.get_for_model(queryset.model)
                    return render(request, 'workon/selection/admin/add.html',
                    {
                        'queryset': Selection.get_queryset_for_ids(content_type, request.POST.get('ids')),
                        'selections': Selection.objects.all(),
                        'form_url': self.get_admin_url('selection_add'),
                        'form': form
                    })
        return self.changelist_view(request)





    def action_selection_save(self, request, queryset):
        ids = ",".join(map(str, queryset.values_list('id', flat=True)))
        content_type = ContentType.objects.get_for_model(queryset.model)
        form = SelectionForm(initial={
            'ids': ids,
            'content_type': content_type,
            # 'user': request.user
        })
        return render(request, self.selection_save_template_name,
        {
            'queryset': Selection.get_queryset_for_ids(content_type, ids),
            'selections': Selection.objects.all(),
            'form_url': self.get_admin_url('selection_save'),
            'queryset': queryset,
            'form': form
        })

    action_selection_save.short_description = u"Sauvegarder la selection"


    def selection_save(self, request, force=False):
        if request.method == "POST":
            if request.POST.get('_selection_save') or force:
                form = SelectionForm(request.POST)
                if form.is_valid():
                    existing_selection = form.cleaned_data.get('existing_selection')
                    if existing_selection:
                        form.instance.created_at = existing_selection.created_at
                        form.instance.pk = form.cleaned_data.get('existing_selection').pk
                    form.instance.user = request.user
                    instance = form.save()
                    self.selection_id = instance.pk

                    messages.success(request, u"Selection \"%s\" enregistrée avec succés" % instance.name )
                else:
                    content_type = ContentType.objects.get_for_model(queryset.model)
                    return render(request, 'workon/selection/admin/save.html',
                    {
                        'queryset': Selection.get_queryset_for_ids(content_type, request.POST.get('ids')),
                        'selections': Selection.objects.all(),
                        'form_url': self.get_admin_url('selection_save'),
                        'form': form
                    })
        return self.changelist_view(request)


    def changelist_view(self, request, extra_context=None):

        extra_context = extra_context or {}
        return super(SelectionAdmin, self).changelist_view(request, extra_context=extra_context)



    # def action_selection_load(self, request, queryset):

    #     return render_to_response('workon/selection/admin/load.html', RequestContext(request,
    #     {
    #         'selections': Selection.objects.all(),
    #     }))

    # action_selection_load.short_description = u"Charger une selection"

