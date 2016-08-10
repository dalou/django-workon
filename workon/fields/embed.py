# encoding: utf-8

from django.db import models
from ..forms import EmbedInput

# - Youtube
# - Soundcloud
# - Vimeo
# - Bandcamp
# - Pinterest
# - Mixcloud
# - Dailymotion




class EmbedField(models.TextField):

    def __init__(self, *args, **kwargs):

        self.authorized_types = ['image', 'youtube', 'dailymotion']
        if kwargs.get('authorized_types'):
            self.authorized_types = kwargs.pop('authorized_types')

        kwargs['max_length'] = 255

        super(EmbedField, self).__init__(*args, **kwargs)


    def formfield(self, **kwargs):
        defaults = { 'widget': EmbedInput }
        defaults.update(kwargs)
        # defaults['form_class'] = EmbedField
        defaults['widget'] = EmbedInput(
            attrs = { 'class': 'image-ratio', },
            authorized_types = self.authorized_types,
        )
        return super(EmbedField, self).formfield(**defaults)

