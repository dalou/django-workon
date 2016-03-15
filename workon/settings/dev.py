
########## CUSTOM DEV SERVER OUTPUT
from django.conf import settings
from django.core.servers.basehttp import WSGIRequestHandler
import sys, copy, re

def set_minimal_logs(ignore_extensions=['.png', '.jpg', '.jpeg', '.gif', '.css', '.js']):

    WSGIRequestHandler.old_log_message = copy.deepcopy(WSGIRequestHandler.log_message)

    def log_message(self, format, *args):
        if hasattr(self, 'path'):
            for extension in ignore_extensions:
                if self.path.lower().endswith(extension):
                    return
        self.old_log_message(format, *args)

    WSGIRequestHandler.log_message = log_message
    ########## END CUSTOM DEV SERVER OUTPUT