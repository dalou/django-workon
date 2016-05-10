from django import template
from django.contrib.admin.utils import lookup_field
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.utils.safestring import mark_safe
from ..contrib.admin import config
from ..contrib.admin import utils

from colour import Color

register = template.Library()


@register.filter(name='workon_admin_conf')
def workon_admin_conf(name):
    value = config.get_config(name)
    return mark_safe(value) if isinstance(value, str) else value

@register.filter
def workon_admin_form_tabs(model_admin):
    for attr in ['workon_form_tabs', 'form_tabs', 'suit_form_tabs']:
        if hasattr(model_admin, attr):
            return getattr(model_admin, attr)
    return None


@register.filter
def workon_admin_form_includes(model_admin):
    for attr in ['workon_form_includes', 'form_includes', 'suit_form_includes']:
        if hasattr(model_admin, attr):
            return getattr(model_admin, attr)
    return []


@register.filter
def workon_admin_platform(request):
    if not request:
        return ''
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    css = []

    # OS
    if 'Macintosh' in user_agent:
        css.append('os-macos')
    elif 'Linux' in user_agent:
        css.append('os-linux')
    else:
        css.append('os-win')

    # Browser
    if 'Chrome' in user_agent:
        css.append('br-chrome')
    elif 'Firefox' in user_agent:
        css.append('br-firefox')

    return ' '.join(css)


@register.assignment_tag
def workon_admin_conf_value(name, model_admin=None):
    if model_admin:
        value_by_ma = getattr(model_admin, 'workon_admin_%s' % name.lower(), None)
        if value_by_ma in ('center', 'right'):
            config.set_config_value(name, value_by_ma)
        else:
            config.reset_config_value(name)
    return workon_admin_conf(name)


@register.tag
def workon_admin_date(parser, token):
    return NowNode(config.get_config('HEADER_DATE_FORMAT'))


@register.tag
def workon_admin_time(parser, token):
    return NowNode(config.get_config('HEADER_TIME_FORMAT'))


@register.filter
def field_contents_foreign_linked(admin_field):
    """Return the .contents attribute of the admin_field, and if it
    is a foreign key, wrap it in a link to the admin page for that
    object.

    Use by replacing '{{ field.contents }}' in an admin template (e.g.
    fieldset.html) with '{{ field|field_contents_foreign_linked }}'.
    """
    fieldname = admin_field.field['field']
    displayed = admin_field.contents()
    obj = admin_field.form.instance

    if not hasattr(admin_field.model_admin,
                   'linked_readonly_fields') or fieldname not in admin_field \
            .model_admin \
            .linked_readonly_fields:
        return displayed

    try:
        fieldtype, attr, value = lookup_field(fieldname, obj,
                                              admin_field.model_admin)
    except ObjectDoesNotExist:
        fieldtype = None

    if isinstance(fieldtype, ForeignKey):
        try:
            url = admin_url(value)
        except NoReverseMatch:
            url = None
        if url:
            displayed = "<a href='%s'>%s</a>" % (url, displayed)
    return mark_safe(displayed)


@register.filter
def admin_url(obj):
    info = (obj._meta.app_label, obj._meta.object_name.lower())
    return reverse("admin:%s_%s_change" % info, args=[obj.pk])


@register.simple_tag
def workon_admin_bc(*args):
    return utils.value_by_version(args)


@register.assignment_tag
def workon_admin_bc_value(*args):
    return utils.value_by_version(args)


@register.simple_tag
def workon_admin_theme_hex(request):
    theme = config.get_config('theme')
    theme = request.GET.get('workon_admin_theme', theme)
    theme = request.COOKIES.get('workon_admin_theme', theme)
    theme = theme.replace('%23', '#')
    return theme


@register.assignment_tag
def workon_admin_theme(*args):
    request = args[0]
    theme = config.get_config('theme')
    theme = request.GET.get('workon_admin_theme', theme)
    theme = request.COOKIES.get('workon_admin_theme', theme)
    theme = theme.replace('%23', '#')

    color = None
    light_color1 = "#6F86B3"
    light_color2 = "#657AA2"
    dark_color1 = "#5A6D92"
    dark_color2 = "#374358"

    if theme == "red":

        light_color1 = "#B36F6F"
        light_color2 = "#A26565"
        dark_color1 = "#925A5A"
        dark_color2 = "#583737"

    # elif theme == "yellow":

    #     color1 = "#C3B64E"
    #     light_color1 = Color("#C3B64E")
    #     light_color2 = Color("#C3B64E", luminance=0.4)
    #     dark_color1 = Color("#C3B64E", luminance=0.35)
    #     dark_color2 = Color("#C3B64E", luminance=0.2)

    elif theme.startswith('#'):
        color = Color(theme)
        # if color.luminance <= 0.5:
        light_color1 = Color(theme, saturation=0.7, luminance=0.6)
        light_color2 = Color(theme, luminance=0.4)
        dark_color1 = Color(theme, luminance=0.35)
        dark_color2 = Color(theme, luminance=0.1)
        # else:
        #     dark_color1 = Color(theme)
        #     dark_color2 = Color(theme, luminance=0.4)
        #     light_color1 = Color(theme, luminance=0.35)
        #     light_color2 = Color(theme, luminance=0.2)


    if not color:
        return None
    return {
        'name': theme,
        'color': color,
        'light_color1': light_color1,
        'light_color2': light_color2,
        "dark_color1": dark_color1,
        "dark_color2": dark_color2,
    }
