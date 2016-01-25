# encoding: utf-8

from .extended import *


from ..models import GoogleAPISettings
# from django import template
# from django.conf import settings
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





########################### METAS


from django import template
from django.template import resolve_variable
from django.template.base import FilterExpression
from django.template.loader import get_template
from django.template import engines
from django.conf import settings
import re


# @register.simple_tag
# def meta_title(value):
#     global TEMPLATE_META_TITLE = value


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
        return self.nodelist.render(context)

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






########################### END METAS




import json
from oauth2client.client import SignedJwtAssertionCredentials

try:
    import suit
    suit_version = suit.VERSION

    if 'suit' in settings.INSTALLED_APPS:
        if suit_version <= "0.3":
            ANALYTICS_TEMPLATE = 'workon/analytics/analytics_suit.html'
        else:
            ANALYTICS_TEMPLATE = 'workon/analytics/analytics_suit3.html'
    else:
        ANALYTICS_TEMPLATE = 'workon/analytics/analytics.html'
except:
    ANALYTICS_TEMPLATE = 'workon/analytics/analytics.html'


@register.inclusion_tag(ANALYTICS_TEMPLATE, takes_context=True)
def analytics(context, view_id=None, next = None):

    # The scope for the OAuth2 request.
    SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
    token = ""



    ggsettings = GoogleAPISettings.objects.first()

    if ggsettings and ggsettings.account_key_file:

        if not view_id:
            view_id = "%s" % int(ggsettings.analytics_default_view_id)

        _key_data = json.load(ggsettings.account_key_file)

        # Construct a credentials objects from the key data and OAuth2 scope.
        try:
            _credentials = SignedJwtAssertionCredentials(
                _key_data['client_email'],
                _key_data['private_key'],
                'https://www.googleapis.com/auth/analytics.readonly',
                # token_uri='https://accounts.google.com/o/oauth2/token'
            )
            token = _credentials.get_access_token().access_token
        except Exception, e:
            print e.message
            token = ""


    return {
        'token': token,
        'view_id': view_id
    }

