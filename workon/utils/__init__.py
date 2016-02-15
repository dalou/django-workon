from ..paginator import Paginator
from .date import *
from .email import *
from .url import *
from .text import *
from .file import *
from .geo import *
from .color import *
from .tree import *
from .rss import *
from .crypt import *
from ..modules.chart.utils import register_chart
from ..modules.stripe.utils import stripe_charge_plan
from .user import get_or_create_user, authenticate_user

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