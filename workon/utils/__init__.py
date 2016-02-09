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
from ..modules.chart.utils import register_chart


from django.conf import settings
def get_project_title(default=""):
    for attr in ['PROJECT_NAME', 'APP_NAME', 'BASE_DIR', 'SITE_NAME', 'SITE_ROOT']:
        if hasattr(settings, attr):
            return getattr(settings, attr).capitalize()
    return default