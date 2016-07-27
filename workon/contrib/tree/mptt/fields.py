"""
Model fields for working with trees.
"""
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from .forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField


__all__ = ('TreeForeignKey', 'TreeOneToOneField', 'TreeManyToManyField')


class TreeForeignKey(models.ForeignKey):
    """
    Extends the foreign key, but uses mptt's ``TreeNodeChoiceField`` as
    the default form field.

    This is useful if you are creating models that need automatically
    generated ModelForms to use the correct widgets.
    """

    def formfield(self, **kwargs):
        """
        Use MPTT's ``TreeNodeChoiceField``
        """
        kwargs.setdefault('form_class', TreeNodeChoiceField)
        return super(TreeForeignKey, self).formfield(**kwargs)


class TreeOneToOneField(models.OneToOneField):
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', TreeNodeChoiceField)
        return super(TreeOneToOneField, self).formfield(**kwargs)


class TreeManyToManyField(models.ManyToManyField):
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', TreeNodeMultipleChoiceField)
        return super(TreeManyToManyField, self).formfield(**kwargs)

# South integration
if 'south' in settings.INSTALLED_APPS:  # pragma: no cover
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^mptt\.fields\.TreeForeignKey"])
    add_introspection_rules([], ["^mptt\.fields\.TreeOneToOneField"])
    add_introspection_rules([], ["^mptt\.fields\.TreeManyToManyField"])
