# encoding: utf-8

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

WORKON_CHARTS = {}

def highchart_render(context, *args, **kwargs):
    if args:
        chart = WORKON_CHARTS.get(args[0])
        if chart:
            return {
                'chart': chart.get('method')(context, *args, **kwargs),
                'label': kwargs.get('label', chart.get('label',  ''))
            }

register.inclusion_tag('workon/chart/highchart_chart.html', takes_context=True, name='highchart_render')(highchart_render)
