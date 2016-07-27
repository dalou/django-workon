# encoding: utf-8

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import six

from django import forms
from itertools import chain
from .mptt.models import MPTTModel, TreeForeignKey
from .mptt.managers import TreeManager

class TreeManager(TreeManager):
    _tree = None
    _trees = {}

    def filters(self, **kwargs):
        return []

    def get_tree(self, root=None, queryset=None):
        if self._tree is None:
            self.build_tree(queryset=queryset)
        return self._tree

    def get_children(self, root=None):
        if self._tree is None:
            self.build_tree()
        if root:
            elm = self._tree_by_id.get(root.id)
            if elm:
                return elm._children
            else:
                return []
        else:
            return self.get_tree()

    def get_filtered_selection(self, selection, root=None, include_level=-1, exclude_parent=True, final_selection=None, filter={}, exclude={}):

        if root:
            tree = root.get_children()
        else:
            tree = self.get_tree()


        # print 'get_filtered_selection TREE', tree
        if selection is None:
            return []

        if isinstance(selection, six.string_types):
            selection = selection.split(',')

        _selection = []
        for s in selection:
            s = str(s).strip()
            if s != "":
                _selection.append(int(s))

        # print 'selection', tree, _selection

        _final_selection = final_selection if final_selection else {}
        root_empty = True
        for child in tree:
            if child.pk in _selection:
                _final_selection[child.pk] = child
                root_empty = False

                if exclude_parent and child.parent_id and _final_selection.get(child.parent_id):
                    del _final_selection[child.parent_id]

                self.get_filtered_selection(selection, root=child, include_level=include_level, exclude_parent=exclude_parent, final_selection=_final_selection, filter=filter, exclude=exclude)

        if include_level and root_empty:
            for child in tree:
                _final_selection[child.pk] = child
                if include_level >= 1 or include_level == -1:
                    self.get_filtered_selection(selection, root=child, include_level=include_level-1, exclude_parent=exclude_parent, final_selection=_final_selection, filter=filter, exclude=exclude)

        return _final_selection.keys()

    def build_tree(self, queryset=None):
        if queryset:
            roots = queryset.prefetch_related('children').select_related('parent').distinct()
        else:
            roots = self.filter(**self.model._tree_filters).prefetch_related('children').select_related('parent')

        _tree_by_id = {}
        _tree = []
        for elm in roots:
            elm._children = []
            _tree_by_id[elm.pk] = elm
        for pk, elm in _tree_by_id.items():
            if elm.parent_id:
                parent = _tree_by_id.get(elm.parent_id)
                # print parent
                # element.parent = parent
                if parent:
                    if not hasattr(parent, '_children'):
                        setattr(parent, '_children', [])
                    parent._children.append(elm)
            else:
                _tree.append(elm)
        self._tree_by_id = _tree_by_id
        self._tree = _tree
        # print 'BUILD TREE'


class Tree(MPTTModel):

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    order = models.IntegerField(u"Ordre", default=0)

    is_required = models.BooleanField(u"Requit ?", default=False)
    is_independant = models.BooleanField(u"Indépendant ?", default=False)
    is_multiple = models.BooleanField(u"Choix multiple ?", default=False)

    _tree_default_queryset = None
    _tree_auto_rebuild = True
    _tree_filters = {}

    objects = models.Manager()
    tree = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        abstract = True
        ordering = ('tree_id', 'lft')
        verbose_name = u'Catégorie'
        verbose_name_plural = u'Catégories'


    def save(self, *args, **kwargs):
        # if self.parent:
        #     self.level = self.parent.level + 1
        super(Tree, self).save(*args, **kwargs)
        # if self.__class__._tree_auto_rebuild:
        #     self.__class__.tree.tree = None
        #     self.__class__.tree.trees = None

    def get_children(self, include_self=False):
        children = self.__class__.tree.get_children(self)
        if include_self:
            children.append(self)
        return children

    def is_leaf_node(self):
        return not self.get_descendant_count()

    def get_descendant_count(self):
        if self.rght is None:
            return 0
        else:
            return ((self.rght - self.lft) - 1) // 2

    # @classmethod
    # def get_root_tree(cls, root=None, queryset=None):


