# encoding: utf-8

from django.conf import settings

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import conditional_escape, format_html, html_safe, escape
from django.utils.encoding import force_text, smart_text, smart_unicode, force_unicode
from django.forms.utils import flatatt, to_current_timezone
from django.utils.safestring import mark_safe
from django.utils import six
from itertools import chain
from collections import OrderedDict

class TreeModelChoiceIterator(forms.models.ModelChoiceIterator):
    def choice(self, obj):
        # tree_id = getattr(obj, getattr(self.queryset.model._meta, 'tree_id_atrr', 'tree_id'), 0)
        # left = getattr(obj, getattr(self.queryset.model._meta, 'left_atrr', 'lft'), 0)
        parent_id = getattr(obj, 'parent_id', None)
        level = getattr(obj, getattr(self.queryset.model._meta, 'level_attr', 'level'), 1)
        return super(TreeModelChoiceIterator, self).choice(obj) + (parent_id, level)

class TreeSelect(forms.Select):

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs['value'] = force_text(value)
        final_attrs['type'] = "hidden"
        output = [
            """<div id="id_tree_%s" class="workon-tree-input" data-tree='{}'>""" % name,
            format_html('<input {} />', flatatt(final_attrs))
        ]

        selects = {}
        tree = {}


        # for choice in chain(self.choices, choices):

        #     if len(choice) < 3:
        #         choice = choice + (None, 0, )
        #     tree[choice[0]] = choice

        for choice in chain(self.choices, choices):

            if len(choice) < 3:
                choice = choice + (None, 0, )
            option_value, option_label, parent_id, level = choice

            option_label = option_label.strip('-')

            if not parent_id:
                parent_id = 0

            select = selects.get(parent_id)
            if not select:
                select = [level, """<div style="%s margin-left:%spx;" class="workon-tree-select" data-tree-level="%s" data-tree-parent="%s"><select>""" % (
                    "display:none;" if parent_id else "",
                    level*50,
                    level,
                    parent_id
                )]
            select[1] += """<option value="%s" data-tree-parent="%s">%s</option>""" % (
                option_value,
                parent_id,
                option_label
            )

            selects[parent_id] = select

        selects = OrderedDict(sorted(selects.items(), key=lambda t: t[0], reverse=False))

        for parent_id, select in selects.items():
            output.append(select[1] + "</select></div>")

        output.append('</div>')
        output.append("""
            <script type="text/javascript">
                $('#id_%(name)s')[0].workon_tree_has_changed = function(value)
                {
                    var option = $('#id_tree_%(name)s option[value="'+value+'"]');
                    option.prop('selected', true);

                    // Children default uncollapse
                    var child = $('#id_tree_%(name)s [data-tree-parent="'+value+'"]').show().find('select');
                    while(child.length)
                    {
                        var empty_value = child.val();
                        child = $('#id_tree_%(name)s [data-tree-parent="'+empty_value+'"]').show().find('select');
                    }

                    // Parent selected uncollapse
                    var select = option.parent();
                    var parent_id = select.parent().show().data('tree-parent');
                    if(parent_id && parent_id != "0")
                    {
                        $('#id_%(name)s')[0].workon_tree_has_changed(parent_id);
                    }
                }

                $('#id_tree_%(name)s').on('change', 'select, .select2', function(values)
                {
                    $('#id_tree_%(name)s [data-tree-parent]').hide();
                    $('#id_%(name)s')[0].workon_tree_has_changed($(this).val());
                    $('#id_%(name)s').val($('#id_tree_%(name)s select:visible').eq(-1).val());
                });

                //$('#id_tree_%(name)s [data-tree-parent]').hide();
                $('#id_%(name)s')[0].workon_tree_has_changed($('#id_%(name)s').val());
            </script>
        """ % { 'name' : name })
        return mark_safe('\n'.join(output))


class TreeModelChoiceField(forms.ModelChoiceField):
    widget = TreeSelect

    def label_from_instance(self, obj):
        level = getattr(obj, getattr(self.queryset.model._meta, 'level_attr', 'level'), 0)
        return u'%s %s' % ('-'*level, smart_unicode(obj))

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return TreeModelChoiceIterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)


    def clean(self, value):

        value = super(TreeModelChoiceField, self).clean(value)

        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
        elif not self.required and not value:
            return None

        if value and not value.is_leaf_node():
            raise ValidationError(u"Vous devez sélectionner une catégorie", code='list')
        else:
            return value