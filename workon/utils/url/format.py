# encoding: utf-8
import re

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

_url_composite = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
_url_regex = re.compile(_url_composite)
_url_regex_multiline = re.compile(_url_composite, re.MULTILINE|re.UNICODE)

__all__ = [
    'append_protocol',
    'extract_urls',
    'urls_to_html',
    'extract_urls_to_html',
    'replace_urls_to_href',
    'get_current_site_domain',
    'build_absolute_url'
]

def append_protocol(url):
    if url:
        if not (url.startswith('http://') or url.startswith('https://')):
            url = "http://%s" % url
    return url

def extract_urls(text):
    if text is not None:
        urls = []
        for url in _url_regex.findall(text):
            if not url.startswith('//'):
                urls.append(append_protocol(url))

        return list(set(urls))
    else:
        return []

def urls_to_html(urls, reverse=True, target="_blank", hide_protocol=True, classname=None, divider="<br />"):

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

def extract_urls_to_html(text, **kwargs):
    return urls_to_html(extract_urls(text), **kwargs)


def replace_urls_to_href(text, target="_blank", hide_protocol=True):

    text = _url_regex_multiline.sub(r'<a href="http://\1" %s rel="nofollow">\1</a>' % (
        ('target="%s" ' % target) if target else ""
    ), text)
    text = text.replace('http://http', 'http')
    # Replace email to mailto
    # urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE|re.UNICODE)
    # value = urls.sub(r'<a href="mailto:\1">\1</a>', value)
    return text

# urlfinder = re.compile("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+):[0-9]*)?/[-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]*[^]'\\.}>\\),\\\"]")

# def urlify2(value):
#     return urlfinder.sub(r'<a href="\1">\1</a>', value)

def get_current_site_domain(request=None):
    if not request:
        try:
            from django.contrib.sites.models import Site
            domain = Site.objects.get_current().domain
        except:
            domain = getattr(settings, 'PROJECT_DOMAIN', '')
    else:
        domain = get_current_site().domain
    return domain

def build_absolute_url(url="", request=None):
    domain = get_current_site_domain(request=request)
    return "{0}://{1}{2}".format(
        getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http"),
        domain.split('//')[-1],
        url
    ).strip('/')