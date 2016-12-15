
# from tinymce.models import HTMLField as TinyMceHTMLField

from django.db import models
from ..forms import (
    DateTimeField as DateTimeFormField,
    DateField as DateFormField,
    DateInput,
    DateTimeInput
)

class DateTimeField(models.DateTimeField):
    """
    A large string field for HTML content. It uses the TinyMCE widget in
    forms.
    """

    def formfield(self, *args, **kwargs):
        kwargs['form_class'] = DateTimeField
        #kwargs['widget'] = DateTimeFormField

        return super(DateTimeField, self).formfield(*args, **kwargs)


class DateField(models.DateField):


    def formfield(self, *args, **kwargs):
        kwargs['form_class'] = DateFormField
        # kwargs['widget'] = DateInput

        return super(DateField, self).formfield(*args, **kwargs)

# try:
#     from south.modelsinspector import add_introspection_rules
#     add_introspection_rules([], ["^workon\.fields\.HtmlField"])
# except ImportError:
#     pass