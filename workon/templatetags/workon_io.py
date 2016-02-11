# -*- coding: utf-8 -*-

from django.conf import settings
from django import template
from ..utils import base64_crypted_key

register = template.Library()

@register.simple_tag(takes_context=True)
def workon_io_connect(context):
    user = context['request'].user
    if hasattr(settings, 'WORKON_IO_KEY'):
        key = base64_crypted_key(user.email, passphrase=getattr(settings, 'WORKON_IO_KEY'))
        if key:
            url = "http://127.0.0.1:8000/connect/%s/?internaladmin=1" % key
            return u"""
            <iframe id="workon-io-iframe" src="%s" style="margin:-20px 0px 0px 0px; width:100%%; min-height:900px; border:0px; padding:0px;"></iframe>
            <script>
                $('#page-content-wrapper').prepend($('#workon-io-iframe'))
            </script>

            """ % url
    return ""