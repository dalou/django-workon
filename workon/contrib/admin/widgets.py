import json
from django.contrib.admin import widgets as admin_widgets
from django.forms import widgets as form_widgets
from django.forms import TextInput, Select, Textarea, fields
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django import forms
from django.utils import formats, translation
from django.utils.translation import ugettext as _
from django.contrib.admin.templatetags.admin_static import static
from . import utils


class LinkedSelect(Select):
    """
    Linked select - Adds link to foreign item, when used with foreign key field
    """

    def __init__(self, attrs=None, choices=()):
        attrs = _make_attrs(attrs, classes="linked-select")
        super(LinkedSelect, self).__init__(attrs, choices)


class EnclosedInput(TextInput):
    """
    Widget for bootstrap appended/prepended inputs
    """

    def __init__(self, attrs=None, prepend=None, append=None):
        """
        For prepend, append parameters use string like %, $ or html
        """
        self.prepend = prepend
        self.append = append
        super(EnclosedInput, self).__init__(attrs=attrs)

    def enclose_value(self, value):
        """
        If value doesn't starts with html open sign "<", enclose in add-on tag
        """
        cls = 'addon'
        if value.startswith("<"):
            cls = 'btn'
        if value.startswith("glyphicon-"):
            value = '<i class="glyphicon %s"></i>' % value
        return '<span class="input-group-%s">%s</span>' % (cls, value)

    def render(self, name, value, attrs=None):
        output = super(EnclosedInput, self).render(name, value, attrs)
        div_classes = []
        if self.prepend:
            # div_classes.append('input-prepend')
            self.prepend = self.enclose_value(self.prepend)
            output = ''.join((self.prepend, output))
        if self.append:
            # div_classes.append('input-append')
            self.append = self.enclose_value(self.append)
            output = ''.join((output, self.append))

        return mark_safe(
            '<div class="input-group %s">%s</div>' % (
                ' '.join(div_classes), output))


class AutosizedTextarea(Textarea):
    """
    Autosized Textarea - textarea height dynamically grows based on user input
    """

    def __init__(self, attrs=None):
        new_attrs = _make_attrs(attrs, {"rows": 2}, "autosize")
        super(AutosizedTextarea, self).__init__(new_attrs)

    @property
    def media(self):
        return forms.Media(js=[static("cago/admin/js/jquery.autosize-min.js")])

    def render(self, name, value, attrs=None):
        output = super(AutosizedTextarea, self).render(name, value, attrs)
        output += mark_safe(
            "<script type=\"text/javascript\">Workon.$('#id_%s').autosize("
            ");</script>"
            % name)
        return output


class DateMixin(object):

    @property
    def media(self):
        # js = ['datepicker/bootstrap-datepicker.js']
        # dp_lang = self.language()
        # if dp_lang != 'en':
        #     js.append('datepicker/locales/bootstrap-datepicker.%s.js' % dp_lang)

        return forms.Media(
            js=[
                'workon/vendors/datetimepicker/jquery.datetimepicker.js',
            ],
            css={'all': ["workon/vendors/datetimepicker/jquery.datetimepicker.css"]}
        )

        input_type = 'date'


    def render_script(self, id):
        return '''<script type="text/javascript">

                    $('#%(id)s').on('mousedown', function() {
                        if(!this.datetimepicker) {
                            $(this).datetimepicker($(this).data('datetime-input'));
                            this.datetimepicker = true;
                        }
                    });
                </script>
                ''' % { 'id' : id }


    def render(self, name, value, attrs={}):
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name

        attrs['class'] += " form-control"
        render = super(DateWidget, self).render(name, value, attrs)
        return mark_safe("%s%s" % (render, self.render_script(attrs['id'])))



class DateWidget(forms.DateInput, DateMixin):

    timepicker = False


    def __init__(self, *args, **kwargs):
        include_seconds = kwargs.pop('include_seconds', False)
        kwargs['format'] = "%d/%m/%Y"
        options = kwargs.pop('options', {
            'lang': 'fr',
            'timepicker': False,
            'mask': False,
            'format': 'd/m/Y'
        })
        super(DateWidget, self).__init__(*args, **kwargs)
        # if not include_seconds:
        #     self.format = re.sub(':?%S', '', self.format)
        attrs = {
            'data-datetime-input': json.dumps(options)
        }
        self.attrs.update(attrs)



class DateTimeWidget(forms.DateTimeInput, DateMixin):
    timepicker = True
    def __init__(self, *args, **kwargs):
        include_seconds = kwargs.pop('include_seconds', True)

        kwargs['format'] = "%d/%m/%Y %H:%M:%S"
        super(DateTimeWidget, self).__init__(*args, **kwargs)
        options = kwargs.pop('options', {
            'lang': 'fr',
            'timepicker': True,
            'mask': False,
            'format': 'd/m/Y H:i:s'
            #'format': 'd.m.Y'
        })
        attrs = {
            'data-datetime-input': json.dumps(options)
        }
        self.attrs.update(attrs)


class WorkonTimeWidget(admin_widgets.AdminTimeWidget):
    def __init__(self, attrs=None, format=None):
        defaults = {'placeholder': _('Time:')[:-1]}
        new_attrs = _make_attrs(attrs, defaults, "vTimeField input-small")
        super(WorkonTimeWidget, self).__init__(attrs=new_attrs, format=format)

    def render(self, name, value, attrs=None):
        output = super(WorkonTimeWidget, self).render(name, value, attrs)
        return mark_safe(
            '<div class="input-append suit-date suit-time">%s<span '
            'class="add-on"><i class="icon-time"></i></span></div>' %
            output)


class WorkonSplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """

    def __init__(self, attrs=None):
        widgets = [DateWidget, WorkonTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        out_tpl = '<div class="datetime">%s %s</div>'
        return mark_safe(out_tpl % (rendered_widgets[0], rendered_widgets[1]))


def _make_attrs(attrs, defaults=None, classes=None):
    result = defaults.copy() if defaults else {}
    if attrs:
        result.update(attrs)
    if classes:
        result["class"] = " ".join((classes, result.get("class", "")))
    return result


def wrap_as_input_group(s, append=''):
    return mark_safe('<div class="input-group">%s</div>%s' % (s, append))


def add_bs3_markup():
    def _build_attrs(self, *args, **kwargs):
        """
        Merge bs3_class attribute with existing class
        """
        attrs = self.build_attrs_original(*args, **kwargs) or {}
        bs3_class = attrs.pop('bs3_class', '')
        if bs3_class:
            css_class = attrs.get('class')
            css_classes = [css_class] if css_class else []
            css_classes.append(bs3_class)
            attrs['class'] = ' '.join(css_classes)
        return attrs


    def _widget_attrs(self, widget):
        """
        Add Bootstrap 3 form-control CSS class
        """
        apply_to = (fields.CharField, fields.BaseTemporalField,
                    fields.IntegerField, fields.ChoiceField)
        attrs = self.widget_attrs_original(widget) or {}
        if issubclass(self.__class__, apply_to) and not \
                issubclass(widget.__class__, (
                        form_widgets.HiddenInput, form_widgets.RadioSelect)):
            attrs.update({'bs3_class': 'form-control'})
        return attrs

    # Override widget_attrs and build_attrs globally to add form-control class
    fields.Field.widget_attrs_original = fields.Field.widget_attrs
    fields.Field.widget_attrs = _widget_attrs
    form_widgets.Widget.build_attrs_original = form_widgets.Widget.build_attrs
    form_widgets.Widget.build_attrs = _build_attrs

    ###########
    #
    # Adjust markup for special widgets
    # I monkey patched, to support all the inherited classes in 3rd party apps
    #

    # Select dropdown + PLUS button
    def render_RelatedFieldWidgetWrapper(self, name, value, *args, **kwargs):
        """
        Method is a clone from original widget, with adjusted markup
        """
        from django.contrib.admin.views.main import TO_FIELD_VAR

        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.model_name)
        self.widget.choices = self.choices
        output = ['<div class="input-group">',
                  self.widget.render(name, value, *args, **kwargs)]
        if self.can_add_related:
            related_url = reverse('admin:%s_%s_add' % info,
                                  current_app=self.admin_site.name)
            url_params = '?%s=%s' % (
                TO_FIELD_VAR, self.rel.get_related_field().name)
            # TODO: "add_id_" is hard-coded here. This should instead use the
            # correct API to determine the ID dynamically.
            output.append(
                '<span class="input-group-btn">'
                '<a href="%s%s" class="add-another btn btn-default" '
                'id="add_id_%s" onclick="return showAddAnotherPopup(this);" '
                'title="%s"><span class="glyphicon glyphicon-plus-sign '
                'color-success"></span></a></span>'
                % (related_url, url_params, name, _('Add Another')))

        output.append('</div>')
        return mark_safe(''.join(output))

    admin_widgets.RelatedFieldWidgetWrapper.render = \
        render_RelatedFieldWidgetWrapper

    # Select dropdown + PLUS button
    def render_ForeignKeyRawIdWidget(self, name, value, attrs=None):
        rel_to = self.rel.to
        if attrs is None:
            attrs = {}
        extra = []
        if rel_to in self.admin_site._registry:
            # The related object is registered with the same AdminSite
            related_url = reverse(
                'admin:%s_%s_changelist' % (
                    rel_to._meta.app_label,
                    rel_to._meta.model_name,
                ),
                current_app=self.admin_site.name,
            )

            params = self.url_parameters()
            if params:
                url = '?' + '&amp;'.join(
                    '%s=%s' % (k, v) for k, v in params.items())
            else:
                url = ''
            if "class" not in attrs:
                attrs['class'] = 'vForeignKeyRawIdAdminField'
                # The JavaScript code looks for this hook.
            # TODO: "lookup_id_" is hard-coded here. This should instead use
            # the correct API to determine the ID dynamically.
            extra.append(
                '<span class="input-group-btn"><a href="%s%s" '
                'class="related-lookup btn btn-default" id="lookup_id_%s" '
                'onclick="return showRelatedObjectLookupPopup(this);" '
                'title="%s"><span class="glyphicon '
                'glyphicon-search"></span></a></span>' %
                (related_url, url, name, _('Lookup')))

        output = ['<div class="input-group">',
                  super(self.__class__, self).render(name, value, attrs)]
        output.extend(extra)
        output.append('</div>')
        if value:
            output.append(self.label_for_value(value))

        return mark_safe(''.join(output))

    admin_widgets.ForeignKeyRawIdWidget.render = render_ForeignKeyRawIdWidget
