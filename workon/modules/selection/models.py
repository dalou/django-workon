from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from ...fields import JSONField

class Selection(models.Model):

    name = models.CharField(u"Nom", max_length=254)
    description = models.TextField(u"Description", max_length=254)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    ids = models.TextField(u"ids", default="")

    def __str__(self):
        return self.name

    def set_content_type(self, model, save=True):
        self.content_type = ContentType.objects.get_for_model(model)
        if save:
            self.save()


    def set_selection(self, queryset, save=True):
        if isinstance(queryset, list):
            self.ids = ",".join(list(set(map(int, queryset))))
        else:
            self.ids = ",".join(queryset.values_list('id', flat=True))
        if save:
            self.save()
        return self.ids

    def get_ids(self):
        return list(set(map(int, self.ids.split(','))))

    def get_queryset(self):
        return self.content_type.model_class().objects.filter(pk__in=self.get_ids())

    def get_absolute_admin_url(self, args=None):
        opts = self.content_type.model_class()._meta
        print opts
        url_name = 'admin:%s_%s_%s' % (opts.app_label, self.content_type.model_class().__class__.__name__)

        return "%s?_selection_load=%s" % (reverse(
            url_name,
            args=args,
        ), self.id)