import os, functools

from .format import (
    extract_urls,
    urls_to_html,
    extract_urls_to_html,
    replace_urls_to_href,
    get_current_site_domain,
    build_absolute_url
)

from django.core import urlresolvers
from django.core.exceptions import SuspiciousOperation
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


def default_redirect(request, fallback_url, **kwargs):
    redirect_field_name = kwargs.get("redirect_field_name", "next")
    next_url = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name))
    if not next_url:
        # try the session if available
        if hasattr(request, "session"):
            session_key_value = kwargs.get("session_key_value", "redirect_to")
            if session_key_value in request.session:
                next_url = request.session[session_key_value]
                del request.session[session_key_value]
    is_safe = functools.partial(
        ensure_safe_url,
        allowed_protocols=kwargs.get("allowed_protocols"),
        allowed_host=request.get_host()
    )
    if next_url and is_safe(next_url):
        return next_url
    else:
        try:
            fallback_url = urlresolvers.reverse(fallback_url)
        except urlresolvers.NoReverseMatch:
            if callable(fallback_url):
                raise
            if "/" not in fallback_url and "." not in fallback_url:
                raise
        # assert the fallback URL is safe to return to caller. if it is
        # determined unsafe then raise an exception as the fallback value comes
        # from the a source the developer choose.
        is_safe(fallback_url, raise_on_fail=True)
        return fallback_url


def ensure_safe_url(url, allowed_protocols=None, allowed_host=None, raise_on_fail=False):
    if allowed_protocols is None:
        allowed_protocols = ["http", "https"]
    parsed = urlparse(url)
    # perform security checks to ensure no malicious intent
    # (i.e., an XSS attack with a data URL)
    safe = True
    if parsed.scheme and parsed.scheme not in allowed_protocols:
        if raise_on_fail:
            raise SuspiciousOperation("Unsafe redirect to URL with protocol '{0}'".format(parsed.scheme))
        safe = False
    if allowed_host and parsed.netloc and parsed.netloc != allowed_host:
        if raise_on_fail:
            raise SuspiciousOperation("Unsafe redirect to URL not matching host '{0}'".format(allowed_host))
        safe = False
    return safe
