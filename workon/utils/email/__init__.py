
# encoding: utf-8

import datetime
import operator
import hashlib
import random
import re
from email.utils import parseaddr
import functools
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:  # python 2
    from urlparse import urlparse, urlunparse

from django.db import models
from django.db.models import Q
from django.contrib import auth, messages
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.utils.html import strip_tags
from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib.auth import get_user_model
from premailer import transform

_email_regex = re.compile("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)")

def extract_emails(text):
    if text is not None:
        return list(set((email[0] for email in _email_regex.findall(text) if not email[0].startswith('//'))))
    else:
        return []


def emails_to_html(emails, reverse=True, classname=None, divider="<br />"):
    emails = [
        u'<a href="mailto:%s" %s/>%s</a>' % (
            email,
            ('class="%s" ' % classname) if classname else "",
            email.strip('/')
        ) for email in emails
    ]
    if reverse:
        emails.reverse()
    html = divider.join(emails)
    return html

def extract_emails_to_html(text, **kwargs):
    return emails_to_html(extract_emails(text), **kwargs)

def is_valid_email(email):
    if email is None:
        return None
    result = parseaddr(email.strip().lower())
    if '@' in result[1]:
        return result[1]
    else:
        return None

class ContentEmail(EmailMultiAlternatives):
    def __init__(self, subject, content, sender, receivers, content_type=None, context={}, files=[], **kwargs):

        subject = " ".join(subject.splitlines())
        content = kwargs.pop('body', content)
        if type(receivers) == type(str()) or type(receivers) == type(unicode()):
            receivers = [receivers]
        if content_type:
            super(ContentEmail, self).__init__(subject, '', sender, receivers, **kwargs)
        else:
            super(ContentEmail, self).__init__(subject, content, sender, receivers, **kwargs)

        if content_type:
            self.attach_alternative(content, content_type)
        if files:
            for file in files:
                self.attach(*file)

class HtmlTemplateEmail(EmailMultiAlternatives):

    def __init__(self, subject, html, sender, receivers, context={}, files=[], **kwargs):
        if type(receivers) == type(str()) or type(receivers) == type(unicode()):
            receivers = [receivers]

        subject = " ".join(subject.splitlines())
        text_template = strip_tags(html)
        if kwargs.get('clean_html') == True:
            kwargs.pop('clean_html')
            html = clean_html_for_email(html)
        super(HtmlTemplateEmail, self).__init__(subject, text_template, sender, receivers, **kwargs)
        self.attach_alternative(html, "text/html")
        if files:
            for file in files:
                self.attach(*file)

def send_email(subject, sender, receivers, content='', content_type=None, files=[], **kwargs):
    message = ContentEmail(subject, content, sender, receivers, content_type=content_type, files=files, **kwargs)
    return message.send()

def send_mass_email(messages, **kwargs):
    connection = get_connection()
    connection.open()
    connection.send_messages(messages)
    connection.close()

def send_html_email(subject, sender, receivers, html='', context={}, files=[], **kwargs):
    message = HtmlTemplateEmail(subject, html, sender, receivers, context, files=files, **kwargs)
    return message.send()

def send_template_email(subject, sender, receivers, template=None, context={}, files=[], **kwargs):
    html_template = get_template(template)
    context = Context(context)
    html = html_template.render(context)
    return send_html_email(subject, sender, receivers, html=html, context=context, files=files, **kwargs)


def set_mailchimp_vars(template):
    template = template.replace('*|CURRENT_YEAR|*', str(datetime.date.today().year) )
    return template


def clean_html_for_email(html):
    return transform(html)






