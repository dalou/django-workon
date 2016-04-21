# encoding: utf-8

from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import strip_tags
from django.utils.html import escape
from django.template import Context
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext as _
import json
try:
    from django.utils.encoding import smart_text as smart_unicode
except ImportError:
    try:
        from django.utils.encoding import smart_unicode
    except ImportError:
        from django.forms.util import smart_unicode


class CodeField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(CodeField, self).__init__(*args, **kwargs)


class CodeInput(forms.Textarea):

    class Media:
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.3/ace.js',
            'https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.3/mode-html.js',
        ]
        css = {
        }

    def render_script(self, id, mode):
        return u'''
                <div id="%(id)s_ace_editor"></div>
                <script type="text/javascript">


                    ed = ace.edit("%(id)s_ace_editor");
                    ed.setTheme("ace/theme/monokai");
                    ed.getSession().setMode("ace/mode/%(mode)s");
                    ed.setPrintMarginColumn(150)
                    ed.setOptions({
                        maxLines: Infinity
                    });
                    ed.resize();
                    ed.on("change", function(e) {
                        $('#%(id)s').val(ed.getValue());
                    });
                    ed.setValue($('#%(id)s').val())

                </script>
                ''' % { 'id' : id, 'mode': mode }


    def render(self, name, value, attrs={}):
        print attrs
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name
        if 'mode' not in attrs:
            attrs['mode'] = "python"
        attrs['style'] = "display:none;"
        render = super(CodeInput, self).render(name, value, attrs)
        return mark_safe("%s%s" % (render, self.render_script(attrs['id'], attrs['mode'])))