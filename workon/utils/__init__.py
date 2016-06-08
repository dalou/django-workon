from ..contrib.paginator import Paginator, DiggPaginator
from .date import *
from .url import *
from .text import *
from .file import *
from .geo import *
from .color import *
from .tree import *
from .cache import *
from .number import *
from .rss import *
from .crypt import *
from .email import *
from ..contrib.google.utils import *
from ..contrib.chart.utils import register_chart
from ..contrib.stripe.utils import *
from ..contrib.auth.utils import get_activation_token, get_valid_activation_token, create_activation_token, get_or_create_user, authenticate_user

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

def jsonify(obj):
    if obj is None:
        return "{}"
    if isinstance(obj,dict):
        return json.dumps(obj)
    elif isinstance(obj,list):
        return json.dumps(obj)
    else:
        # obj = re.sub(r'([\w\d_]+)\:', '"\\1":', obj)
        obj = re.sub(r'\'', '"', obj)
        obj = re.sub(r'\/\/\s*[\w\s\d]+', '', obj)
        obj = re.sub(r'Date\.UTC\(.+\)', '""', obj)

        try:
            return json.dumps(json.loads(obj))
        except:
            return json.loads(json.dumps(obj))


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')