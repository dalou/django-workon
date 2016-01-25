# encoding: utf-8

import datetime, json
from django import template
from django.utils.safestring import mark_safe

# from .admin_charts import (
#     user_12_months,
#     college_evolution,
#     groups_by_dpt,
#     groups_by_year,
#     google_analytics
# )


HIGHCHARTS = []
register = template.Library()

def register(name, charts):

    register.inclusion_tag('workon/charts/hightchart.html', takes_context=True, name='user_12_months_chart')(user_12_months.chart)


# register.inclusion_tag('app_stats/admin/google_analytics.html', takes_context=True, name='google_analytics_data')(google_analytics.data)
#register.inclusion_tag('statistics/admin/chart.html', takes_context=True, name='user_genders' )(user_genders.chart)
# register.inclusion_tag('statistics/admin/chart.html', takes_context=True)(admin_user_signup_types_graph)
# register.inclusion_tag('statistics/admin/stats_table.html', takes_context=True)(admin_user_stats)
# register.inclusion_tag('statistics/admin/chart.html', takes_context=True)(admin_user_genders_graph)

