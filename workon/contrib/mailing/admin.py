# encoding: utf-8

from django.conf import settings
from django.contrib import admin
from django.db import models
from django import forms
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from .models import *

# class EmailingUserActivationTokenAdmin(admin.ModelAdmin):
#     list_display = ('email', 'token', 'is_used', 'activation_date', 'expiration_date', 'created_date')
#     search_fields = ('email', 'token', 'activation_date', 'created_date' )
#     list_filter = ('is_used', )

#     def get_readonly_fields(self, *args, **kwargs):
#         fields = [f.name for f in self.model._meta.fields]
#         return fields
# admin.site.register(EmailingUserActivationToken, EmailingUserActivationTokenAdmin)


class EmailingTestEmailAdmin(admin.ModelAdmin):
    list_display = ('email', )
admin.site.register(EmailingTestEmail, EmailingTestEmailAdmin)


class EmailingTransactionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'emailing', 'receiver', 'created_date', 'send_count')
    search_fields = ('emailing__email', 'receiver',  )

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, *args, **kwargs):
        return [f.name for f in self.model._meta.fields]
admin.site.register(EmailingTransaction, EmailingTransactionAdmin)



class EmailingForm(forms.ModelForm):

    class Meta:
        model = Emailing
        fields = ('send_count', 'test_count', 'send_range', 'name', 'subject', 'sender', 'template', 'receivers', 'receivers_test',)


    def __init__(self, *args, **kwargs):
        super(EmailingForm, self).__init__( *args, **kwargs)
        self.fields['send_count'].widget.attrs['readonly'] = True
        self.fields['test_count'].widget.attrs['readonly'] = True




class EmailingAdmin(admin.ModelAdmin):
    change_form_template = 'workon/emailing/admin/send_form.html'
    list_display = ('name', 'subject', 'sender', 'get_receivers', 'created_date', 'send_count', 'test_count')

    form = EmailingForm


    def get_receivers(self, obj):
        receivers = obj.receivers.split(',')

        if obj.get_send_count_remind() == 0:
            html = u"""<span style="color:green">"""
        else:
            html = u"""<span style="color:orange">"""

        html += u"%s emails rééllement envoyés</span>" % obj.get_transaction_send_count()
        html += u"""<br />sur %s destinataires réels : %s [..]""" % ( len(receivers), ", ".join(receivers[0:10]))


        return html
    get_receivers.allow_tags = True
    get_receivers.short_description = u"Destinataires"

    def get_changeform_initial_data(self, request, object_id=None):

        receivers = []
        if request.session.get('workon-emailing_receivers'):
            receivers = request.session.get('workon-emailing_receivers')
            del request.session['workon-emailing_receivers']
        return {
            'sender': getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@exemple.fr'),
            'template': 'Template du mail (compatible mailchimp)',
            'receivers': receivers,
            'object': Emailing.objects.get(pk=int(object_id)) if object_id else None,
            'receivers_test': ", ".join(list(set(EmailingTestEmail.objects.all().values_list('email', flat=True))))
        }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.get_changeform_initial_data(request, object_id))
        return super(EmailingAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def response_change(self, request, obj):

        send = '_sendreal' in request.POST or '_sendtest' in request.POST
        test = '_sendtest' in request.POST

        if send:
            receivers = obj.send(force=test, test=test)
            messages.success(request,
                u"%s emails de test vont être envoyés. %s [..]" % (len(receivers), receivers[0:10])
            )

            request.POST['_continue'] = "1"

        return super(EmailingAdmin, self).response_change( request, obj)

admin.site.register(Emailing, EmailingAdmin)



class ExtractEmailingAdmin(object):

    emailing_form_template_name = 'workon/emailing/admin/extract_emailing.html'
    list_emailing = ['workon_extract_emailing']

    def __init__(self, *args, **kwargs):
        super(ExtractEmailingAdmin, self).__init__(*args, **kwargs)
        if not 'workon_extract_emailing' in self.actions:
            self.actions += ('workon_extract_emailing', )


    def extract_emailing(self, request, queryset):
        return []

    def workon_extract_emailing(self, request, queryset):
        emails = self.extract_emailing(request, queryset)
        return render(request, self.emailing_form_template_name,
        {
            'emails': emails,
        })
    workon_extract_emailing.short_description = u"Extraire les emails"





class SendMailMixin(object):

    emailing_form_template_name = 'workon/emailing/admin/send_form.html'

    def __init__(self, *args, **kwargs):
        super(SendMailMixin, self).__init__(*args, **kwargs)
        self.actions += ('send_mail', )

    def send_mail_receivers(self):
        return []

    def send_mail(modeladmin, request, queryset):
        receivers = list(set(modeladmin.send_mail_receivers(request, queryset)))
        request.session['workon-emailing_receivers'] = ", ".join(receivers)
        return redirect(reverse('admin:workon_emailing_add'))
    send_mail.short_description = u"Envoyer un email à la selection"