# # encoding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse, resolve


def save_path(request):
    #if not request
    if not request.path.startswith('/admin/'):
        request.session['workon_admin_front_path'] = request.path

    return {
        'workon_admin_front_path': request.session.get('workon_admin_front_path', None)
    }
