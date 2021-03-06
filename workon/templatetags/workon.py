# encoding: utf-8

from .extended import *


from ..models import GoogleAPISettings
# from django import template
# from django.db.models import Count
# from django.utils import timezone

# register = template.Library()

@register.inclusion_tag('workon/pagination/_digg_pagination.html')
def digg_pagination(objects):
    return {
        'objects': objects,
        'page': objects.number if hasattr(objects, 'number') else None,
        'name': u'Résultat',
        'name_plural': u'Résultats',
    }


@register.simple_tag
def workon_packages_js(*args):
    return """test"""


########################### METAS


from django import template
from django.template.base import FilterExpression
from django.template.loader import get_template
from django.template import engines
from django.conf import settings
from django.utils.safestring import mark_safe
from django.templatetags.static import static as original_static
from django.core.files.images import ImageFile
from django.core.files.storage import get_storage_class, FileSystemStorage
import re, os

from urllib import urlencode
from urlparse import parse_qs, urlsplit, urlunsplit

from ..utils import (
    canonical_url,
    replace_urls_to_href as utils_replace_urls_to_href,
    jsonify as utils_jsonify
)


if "compressor" in settings.INSTALLED_APPS:
    @register.tag
    def compress(parser, token):
        from compressor.templatetags.compress import compress
        return compress(parser, token)
else:
    @register.to_end_tag
    def compress(parsed, context, token):
        return parsed


@register.filter
def absolute_url(url):
    return canonical_url(url)


@register.filter
def replace_urls_to_href(text):
    return mark_safe(utils_replace_urls_to_href(text))

@register.filter
def static(url):
    return original_static(url)

@register.filter
def absolute_static(url):
    return absolute_url(original_static(url))

@register.filter
def static_image(url):
    storage_class = get_storage_class(settings.STATICFILES_STORAGE)
    storage = storage_class()
    image = ImageFile(storage.open(url))
    image.storage = storage
    return image, image.url

@register.filter(name='range')
def range_filter(x):
    return range(x)

if "sorl.thumbnail" in settings.INSTALLED_APPS:
    from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode
    from django.templatetags.static import static
    from django.contrib.staticfiles.storage import staticfiles_storage
    from django.contrib.staticfiles import finders
    from django.utils.six import text_type
    from sorl.thumbnail.shortcuts import get_thumbnail
    from sorl.thumbnail.images import ImageFile, DummyImageFile

    class SafeStaticFilesStorage(get_storage_class(settings.STATICFILES_STORAGE)):
        def path(self, name):
            return os.path.join(self.location, name)

    class StaticThumbnailNode(ThumbnailNode):

        def _render(self, context):
            storage = SafeStaticFilesStorage()
            file_ = self.file_.resolve(context)
            absolute_path = finders.find(file_)
            try:
                file_ = ImageFile(staticfiles_storage.open(file_))
            except:
                file_ = ImageFile(open(absolute_path))
            file_.storage = storage
            geometry = self.geometry.resolve(context)
            options = {}
            for key, expr in self.options:
                noresolve = {'True': True, 'False': False, 'None': None}
                value = noresolve.get(text_type(expr), expr.resolve(context))
                if key == 'options':
                    options.update(value)
                else:
                    options[key] = value

            thumbnail = get_thumbnail(file_, geometry, **options)

            if not thumbnail or (isinstance(thumbnail, DummyImageFile) and self.nodelist_empty):
                if self.nodelist_empty:
                    return self.nodelist_empty.render(context)
                else:
                    return ''

            if self.as_var:
                context.push()
                context[self.as_var] = thumbnail
                output = self.nodelist_file.render(context)
                context.pop()
            else:
                output = thumbnail.url

            return output



    @register.tag
    def thumbnail_static(parser, token):
        return StaticThumbnailNode(parser, token)
else:
    @register.to_end_tag
    def thumbnail_static(parsed, context, token):
        return parsed



@register.filter
def to_int(value):
    return int(value)

@register.filter
def to_string(value):
    return str(value)

@register.filter
def jsonify(obj):
    return utils_jsonify(obj)

@register.filter
def startswith(str, compare):
    return str.startswith(compare)


@register.filter(name='sizify')
def sizify(size):
    """
    Simple kb/mb/gb size snippet for templates:

    {{ product.file.size|sizify }}
    """
    #value = ing(value)
    try:
        value = int(size)
        if value < 512000:
            value = value / 1024.0
            ext = 'kb'
        elif value < 4194304000:
            value = value / 1048576.0
            ext = 'mb'
        else:
            value = value / 1073741824.0
            ext = 'gb'
        return '%s %s' % (str(round(value, 2)), ext)
    except:
        return 'n/a'


def _setup_metas_dict(parser):
    try:
        parser._metas
    except AttributeError:
        parser._metas = {}

class DefineMetaNode(template.Node):
    def __init__(self, name, nodelist, args):
        self.name = name
        self.nodelist = nodelist
        self.args = args

    def render(self, context):
        ## empty string - {% meta %} tag does no output
        return ''

@register.tag(name="meta")
def do_meta(parser, token):

    try:
        args = token.split_contents()
        tag_name, meta_name, args = args[0], args[1], args[2:]
    except IndexError:
        raise template.TemplateSyntaxError, "'%s' tag requires at least one argument (macro name)" % token.contents.split()[0]
    # TODO: check that 'args' are all simple strings ([a-zA-Z0-9_]+)
    r_valid_arg_name = re.compile(r'^[a-zA-Z0-9_]+$')
    for arg in args:
        if not r_valid_arg_name.match(arg):
            raise template.TemplateSyntaxError, "Argument '%s' to macro '%s' contains illegal characters. Only alphanumeric characters and '_' are allowed." % (arg, macro_name)
    nodelist = parser.parse(('endmeta', ))
    parser.delete_first_token()

    ## Metadata of each macro are stored in a new attribute
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    _setup_metas_dict(parser)
    if not meta_name in parser._metas:
        parser._metas[meta_name] = DefineMetaNode(meta_name, nodelist, args)
    return parser._metas[meta_name]

class UseMetaNode(template.Node):
    def __init__(self, meta, filter_expressions, truncate=None):
        self.nodelist = meta.nodelist
        self.args = meta.args
        self.filter_expressions = filter_expressions
        self.truncate = truncate
    def render(self, context):
        for (arg, fe) in [(self.args[i], self.filter_expressions[i]) for i in range(len(self.args))]:
            context[arg] = fe.resolve(context)
        return self.nodelist.render(context).strip()

class NoopNode(template.Node):
    def render(self, context):
        return ''

@register.tag(name="usemeta")
def do_usemeta(parser, token, truncate=None):
    try:
        args = token.split_contents()
        tag_name, meta_name, values = args[0], args[1], args[2:]
    except IndexError:
        raise template.TemplateSyntaxError, "'%s' tag requires at least one argument (macro name)" % token.contents.split()[0]
    try:
        meta = parser._metas[meta_name]
    except (AttributeError, KeyError):
        return NoopNode()
        raise template.TemplateSyntaxError, "Macro '%s' is not defined" % meta_name


    if (len(values) != len(meta.args)):
        raise template.TemplateSyntaxError, "Macro '%s' was declared with %d parameters and used with %d parameter" % (
            meta_name,
            len(meta.args),
            len(values))
    filter_expressions = []
    for val in values:
        if (val[0] == "'" or val[0] == '"') and (val[0] != val[-1]):
            raise template.TemplateSyntaxError, "Non-terminated string argument: %s" % val[1:]
        filter_expressions.append(FilterExpression(val, parser))
    return UseMetaNode(meta, filter_expressions, truncate)



@register.inclusion_tag('workon/metas/header.html', takes_context=True)
def meta_headers(context):
    return context

@register.simple_tag()
def url_replace_param(url, param_name, param_value):

    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return mark_safe(urlunsplit((scheme, netloc, path, new_query_string, fragment)))

@register.filter
def multiply(obj, value):
    return obj * value if obj else ""

# @register.simple_tag()
# def multiply(value, factor, *args, **kwargs):
#     if value is not None:
#         return float(value) * float(factor)
#     return None

@register.simple_tag()
def divide(value, factor, *args, **kwargs):
    if isinstance(value, int) or isinstance(value, float) and factor is not 0:
        return float(value) / float(factor)
    return None

@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


# if "workon.contrib.notification" in settings.INSTALLED_APPS:

#     from workon.contrib.notification.templatetags import *