# encoding: utf-8

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

WORKON_CHARTS = {}

def highchart_render(context, *args, **kwargs):
    if args:
        if isinstance(args[0], dict):
            return {
                'chart': args[0],
                'label': kwargs.get('label', args[0].get('label',  ''))
            }
        else:
            chart = WORKON_CHARTS.get(args[0])
            if chart:
                return {
                    'chart': chart.get('method')(context, *args, **kwargs),
                    'label': kwargs.get('label', chart.get('label',  ''))
                }

register.inclusion_tag('workon/chart/highchart_chart.html', takes_context=True, name='highchart_render')(highchart_render)
