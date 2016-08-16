# encoding: utf-8

import re
import os
import logging

from django.conf import settings
from django import forms as base_forms
from django.template import Context
from django.forms.widgets import ClearableFileInput
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.utils import flatatt

try:
    from sorl.thumbnail.shortcuts import get_thumbnail
except:
    def get_thumbnail(image_url, *args, **kwargs):
        return image_url

logger = logging.getLogger(__name__)

class ImageInput(ClearableFileInput):
    template_name = 'workon/fields/_image_input.html'
    attrs = {'accept': 'image/*'}

    def render(self, name, value, attrs=None):
        """
        Render the ``input`` field based on the defined ``template_name``. The
        image URL is take from *value* and is provided to the template as
        ``image_url`` context variable relative to ``MEDIA_URL``. Further
        attributes for the ``input`` element are provide in ``input_attrs`` and
        contain parameters specified in *attrs* and *name*.
        If *value* contains no valid image URL an empty string will be provided
        in the context.
        """
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))

        image_url = final_attrs.get('value', '')
        image_original_url = None
        image_thumb = None
        if image_url:
            image_original_url = os.path.join(settings.MEDIA_URL, image_url)
            try:
                image_thumb = get_thumbnail(image_url, 'x150', crop='center', upscale=True, format="PNG")
            except IOError as inst:
                logger.error(inst)

        return render_to_string(self.template_name, Context({
            'image_thumb': image_thumb,
            'input_attrs': flatatt(final_attrs),
            'image_url': image_url,
            'image_original_url': image_original_url,
            'image_id': "%s-image" % final_attrs['id'],
            'name': "%s" % final_attrs['name'],
        }))


# unsable ?????????????????
class ImageField(base_forms.ImageField):
    widget = ClearableFileInput
    def __init__(self, *args, **kwargs):

        widget = ImageInput
        kwargs['widget'] = widget

        super(ImageField, self).__init__(*args, **kwargs)

        print self.widget


class CroppedImageInput(base_forms.widgets.TextInput):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'workon/forms/image_cropped.css',
            )
        }
        js = (
            settings.STATIC_URL + 'workon/forms/image_cropped.js',
            # settings.STATIC_URL + 'js/cropper.js',
        )

class CroppedImageField(base_forms.CharField):
    widget = CroppedImageInput
    default_error_messages = {
        'invalid_image': "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
    }
    image_field = None


    def __init__(self, *args, **kwargs):

        required = kwargs.get('required', False)
        widget = kwargs.pop('widget', None)
        self.image_field = kwargs.pop('label')

        # print widget == AdminFileWidget, isinstance(widget, AdminFileWidget), widget
        # print


        # if widget:
        # if widget == AdminFileWidget or isinstance(widget, AdminFileWidget):
        widget = CroppedImageInput( attrs={
            'class': 'image-croppable',
            'data-workon-croppedimage': self.image_field,
            'style': 'display:none;',
        })
        kwargs['widget'] = widget
        kwargs['label'] = ""

        super(CroppedImageField, self).__init__(*args, **kwargs)


    def to_python(self, data):
        return super(CroppedImageField, self).to_python(data)