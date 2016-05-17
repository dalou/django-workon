# encoding: utf-8

import json
import time
import re
import os
import logging

from django import forms
from django.core.validators import EMPTY_VALUES
from django.template import Context
from django.forms.widgets import FileInput as OriginalFileInput
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


class DateField(forms.DateField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = DateInput(
                format="%d/%m/%Y",
                attrs={'placeholder': 'jj/mm/aaaa'})
            kwargs['input_formats'] = ['%m/%d/%Y']
        super(DateField, self).__init__(*args, **kwargs)


class DateTimeField(forms.DateTimeField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = DateTimeInput(
                format="%d/%m/%Y %H:%M",
                attrs={'placeholder': 'jj/mm/aaaa'})
            kwargs['input_formats'] = ['%m/%d/%Y %H:%M']
        super(DateTimeField, self).__init__(*args, **kwargs)


class BaseDateInput(forms.DateTimeInput):
    # Build a widget which uses the locale datetime format but without seconds.
    # We also use data attributes to pass these formats to the JS datepicker.

    timepicker = False

    # class Media:
    #     css = {
    #         'all': ('workon/vendors/datetimepicker/jquery.datetimepicker.css',)
    #     }
    #     js = ('workon/vendors/datetimepicker/jquery.datetimepicker.js',)

    input_type = 'date'
    @property
    def media(self):
        return forms.Media(
            js=[
                'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.13.0/locale/fr.js',
                'workon/admin/js/datepicker/bootstrap-datepicker.js'
            ],
            css={'all': [static("workon/admin/js/datepicker/css/datepicker3.css")]}
        )

    def __init__(self, *args, **kwargs):
        include_seconds = kwargs.pop('include_seconds', False)


        options = kwargs.pop('options', {
            'lang': 'fr',
            'timepicker': self.timepicker,
            'mask': False,
            'format': 'd/m/Y H:i' if self.timepicker else 'd/m/Y'
            #'format': 'd.m.Y'
        })
        super(BaseDateInput, self).__init__(*args, **kwargs)

        # if not include_seconds:
        #     self.format = re.sub(':?%S', '', self.format)
        attrs = {
            'data-workon-date-input': json.dumps(options),
            'type': 'text'
        }
        self.attrs.update(attrs)

    def render_script(self, id):
        return '''<script type="text/javascript">

                    $('#%(id)s').on('mousedown', function() {
                        if(!this.datetimepicker) {
                            $(this).datetimepicker($(this).data('workon-date-input'));
                            this.datetimepicker = true;
                        }
                    });
                </script>
                ''' % { 'id' : id }


    def render(self, name, value, attrs={}):
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name
        render = super(BaseDateInput, self).render(name, value, attrs)
        return mark_safe("%s%s" % (render, self.render_script(attrs['id'])))


class DateInput(BaseDateInput):
    timepicker = False


class DateTimeInput(BaseDateInput):
    timepicker = True

