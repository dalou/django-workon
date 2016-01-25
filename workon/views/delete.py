
from django.conf import settings
from django.http import Http404, HttpResponseRedirect, JsonResponse


class MultipleDelete(object):
    success_url = None
    template_name = "workon/views/delete.html"

    def get_queryset(self):
        queryset = super(MultipleDelete, self).get_queryset()
        ids = self.kwargs.get('ids', '').split(',')
        return queryset.filter(id__in=ids)

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.objects = self.get_queryset()
        self.objects.delete()
        return HttpResponseRedirect(self.get_success_url())

    # Only accept POST for now.
    def post(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            return ''