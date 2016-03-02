import os

from .format import extract_urls, urls_to_html, extract_urls_to_html, replace_urls_to_href, build_absolute_url

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from ..cache import memoize


@memoize
def get_current_site(request=None):
    if request:
        return get_current_site(request)
    else:
        from django.contrib.sites.models import Site
        return Site.objects.get(id=settings.SITE_ID)

def external_url(url):
    if not url.startswith('http://') or not url.startswith('https://'):
        return "http://%s" % url
    return url


def canonical_url(url, domain_check=False):
    """
    Ensure that the url contains the `http://mysite.com` part,
    particularly for requests made on the local dev server
    """

    current_site = get_current_site()
    if not url.startswith('http'):
        url = "http://%s" % os.path.join(current_site.domain, url.lstrip('/'))

    if domain_check:
        url_parts = URL(url)
        current_site_parts = URL(URL().domain(current_site.domain).as_string())
        if url_parts.subdomains()[-2:] != current_site_parts.subdomains()[-2:]:
            raise ValueError("Suspicious domain '%s' that differs from the "
                "current Site one '%s'" % (url_parts.domain(), current_site_parts.domain()))

    return url

def canonical_url_static(url, domain_check=False):# False because of S3
    """
    Ensure that the url contains the `http://mysite.com/STATIC_URL` part,
    particularly for requests made on the local dev server
    """
    if url.startswith('http'):
        return url
    return canonical_url( os.path.join(settings.STATIC_URL, url), domain_check)


def url_signature(resolver_match):
    """
    Convert
        a `django.core.urlresolvers.ResolverMatch` instance
        usually retrieved from a `django.core.urlresolvers.resolve` call
    To
        'namespace:view_name'

    that `django.core.urlresolvers.reverse` can use
    """
    signature = resolver_match.url_name
    if resolver_match.namespace:
        signature = "%s:%s" % (resolver_match.namespace, signature)
    return signature
