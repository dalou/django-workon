import os
from django.conf import settings
from django.contrib.staticfiles import finders

WORKON_TINYMCE_URL = getattr(settings, 'WORKON_TINYMCE_URL', "//tinymce.cachefly.net/4.3/tinymce.min.js")

WORKON_TINYMCE_DEFAULT_CONFIG = getattr(settings, 'WORKON_TINYMCE_DEFAULT_CONFIG',
    {
        # 'theme': "simple",
        'relative_urls': False
    }
)