# encoding: utf-8

from django.db import models
from ..forms import CodeInput

class CodeField(models.TextField):
    """
    A large string field for HTML content. It uses the TinyMCE widget in
    forms.
    """
    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop('mode', 'text')
        super(CodeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = { 'widget': CodeInput }
        defaults.update(kwargs)


        # As an ugly hack, we override the admin widget
        # if defaults['widget'] == admin_widgets.AdminTextareaWidget:
        #     defaults['widget'] = tinymce_widgets.AdminTinyMCE

        defaults['widget'] = CodeInput(attrs={
            'placeholder': self.verbose_name,
            'mode': self.mode
        })

        return super(CodeField, self).formfield(**defaults)
