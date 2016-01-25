from django.db import models
from ..forms.tree import TreeModelChoiceField

class TreeManyToManyField(models.ManyToManyField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': TreeModelChoiceField
        }
        return super(TreeManyToManyField, self).formfield(**defaults)

class TreeForeignKey(models.ForeignKey):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': TreeModelChoiceField
        }
        return super(TreeForeignKey, self).formfield(**defaults)