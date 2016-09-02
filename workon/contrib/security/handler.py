
import logging
import logging.config  # needed when logging_config doesn't start with logging.config
import sys
import warnings
from copy import copy

from django.conf import settings
from django.core import mail
from django.core.mail import get_connection
from django.utils.deprecation import RemovedInNextVersionWarning
from django.utils.module_loading import import_string
from django.views.debug import ExceptionReporter

class DisallowedHostHandler(logging.Handler):
    """An exception log handler that emails log entries to site admins.

    If the request is passed as the first argument to the log record,
    request data will be provided in the email report.
    """

    def __init__(self, include_html=True, email_backend=settings.EMAIL_BACKEND):
        logging.Handler.__init__(self)
        self.include_html = include_html
        self.email_backend = email_backend

    def emit(self, record):

        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = ExceptionReporter(request, is_email=False, *exc_info)
        html_message = reporter.get_traceback_html()


        from workon.contrib.security.models import DisallowedHost
        DisallowedHost.objects.create(
            http_host=request.META.get('HTTP_HOST') if request else None,
            remote_addr=request.META.get('REMOTE_ADDR') if request else None,
            http_x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR') if request else None,
            request_uri=request.META.get('REQUEST_URI') if request else None,
            request_method=request.META.get('REQUEST_METHOD') if request else None,
            query_string=request.META.get('QUERY_STRING') if request else None,
            path_info=request.META.get('PATH_INFO') if request else None,
            http_user_agent=request.META.get('HTTP_USER_AGENT') if request else None,
            html_report=html_message
        )
        # subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        # no_exc_record = copy(record)
        # no_exc_record.exc_info = None
        # no_exc_record.exc_text = None


        # message = "%s\n\n%s" % (self.format(no_exc_record), reporter.get_traceback_text())

        # print html_message
        # self.send_mail(subject, message, fail_silently=True, html_message=html_message)

    # def send_mail(self, subject, message, *args, **kwargs):
    #     mail.mail_admins(subject, message, *args, connection=self.connection(), **kwargs)

    def connection(self):
        return get_connection(backend=self.email_backend, fail_silently=True)

    def format_subject(self, subject):
        """
        Escape CR and LF characters, and limit length.
        RFC 2822's hard limit is 998 characters per line. So, minus "Subject: "
        the actual subject must be no longer than 989 characters.
        """
        formatted_subject = subject.replace('\n', '\\n').replace('\r', '\\r')
        return formatted_subject[:989]