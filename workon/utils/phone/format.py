# encoding: utf-8
import re

_phone_composite =
_url_regex = re.compile(_url_composite)
_url_regex_multiline = re.compile(_url_composite, re.MULTILINE|re.UNICODE)

def extract_phones(text):
    if text is not None:
        return list(set((url for url in _url_regex.findall(text) if not url.startswith('//'))))
    else:
        return []


def phones_to_html(urls, reverse=True, target="_blank", hide_protocol=True, classname=None, divider="<br />"):
    urls = [
        u'<a %shref="%s" %s/>%s</a>' % (
            ('target="%s" ' % target) if target else "",
            url,
            ('class="%s" ' % classname) if classname else "",
            (url.replace('https://', '').replace('http://', '') if hide_protocol else url).strip('/')
        ) for url in urls
    ]
    if reverse:
        urls.reverse()
    html = divider.join(urls)
    return html

def extract_phones_to_html(text, **kwargs):
    return urls_to_html(extract_urls(text), **kwargs)


def format_phones(text):

    # urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
    text = _url_regex_multiline.sub(r'<a href="\1" %s>\1</a>' % (
        ('target="%s" ' % target) if target else ""
    ), text)
    # Replace email to mailto
    # urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE|re.UNICODE)
    # value = urls.sub(r'<a href="mailto:\1">\1</a>', value)
    return text