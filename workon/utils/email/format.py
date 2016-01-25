# encoding: utf-8
import re

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