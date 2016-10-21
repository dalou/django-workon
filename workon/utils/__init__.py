
from .cache import *
from .color import *
from .crypt import *
from .date import *
from .debug import *
from .emails import *
from .file import *
from .geo import *
from .number import *
from .opengraph import *
from .pagination import *
from .phone import *
from .rss import *
from .string import *
from .urls import *


from workon.contrib.notification.utils import *
from workon.contrib.google.utils import *
from workon.contrib.chart.utils import register_chart
from workon.contrib.stripe.utils import *
from workon.contrib.auth.utils import *
from workon.contrib.tree.utils import *


from django.conf import settings

def get_project_title(default=""):
    for attr in ['PROJECT_NAME', 'APP_NAME', 'BASE_DIR', 'SITE_NAME', 'SITE_ROOT']:
        if hasattr(settings, attr):
            return getattr(settings, attr).capitalize()
    return default

def get_project_root(default=""):
    for attr in ['BASE_DIR', 'DJANGO_ROOT', 'SITE_ROOT']:
        if hasattr(settings, attr):
            return getattr(settings, attr)
    return default

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')