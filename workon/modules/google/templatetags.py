import json

from django.conf import settings
from django import template
from .models import GoogleAPISettings
from oauth2client.client import SignedJwtAssertionCredentials

register = template.Library()

try:
    import suit

    suit_place = settings.INSTALLED_APPS.index('suit')
    workon_place = settings.INSTALLED_APPS.index('workon')


    if 'suit' in settings.INSTALLED_APPS and \
        settings.INSTALLED_APPS.index('suit') < settings.INSTALLED_APPS.index('workon'):
        suit_version = suit.VERSION
        if suit_version <= "0.3":
            ANALYTICS_TEMPLATE = 'workon/google/analytics_suit.html'
        else:
            ANALYTICS_TEMPLATE = 'workon/google/analytics_suit3.html'
    else:
        ANALYTICS_TEMPLATE = 'workon/google/analytics.html'
except Exception, e:
    ANALYTICS_TEMPLATE = 'workon/google/analytics.html'

def get_credentials(view_id):
    # The scope for the OAuth2 request.
    SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
    token = ""
    ggsettings = GoogleAPISettings.get()
    if ggsettings and ggsettings.account_key_file:
        if not view_id:
            view_id = "%s" % int(ggsettings.analytics_default_view_id)
        # Construct a credentials objects from the key data and OAuth2 scope.
        try:
            _key_data = json.load(ggsettings.account_key_file)
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
    return token, view_id


@register.inclusion_tag('workon/google/analytics.html', takes_context=True)
def google_analytics_admin(context, view_id=None, next = None):

    token, view_id = get_credentials(view_id)
    return {
        'token': token,
        'view_id': view_id
    }

@register.inclusion_tag('workon/google/analytics_charts.html', takes_context=True)
def google_analytics_admin_charts(context, view_id=None, next = None):

    token, view_id = get_credentials(view_id)
    charts = [
        {
            'title': u'Trafic',
            'resume': u'Sessions et Utilisateurs, 15 derniers jours',
            'query': {
                'ids': 'ga:%s' % view_id,
                'start-date': '15daysAgo',
                'end-date': 'yesterday',
                'metrics': 'ga:sessions,ga:users',
                'dimensions': 'ga:date'
            },
            'chart': {
                'type': 'LINE',
            }
        },
        {
            'title': u'Populaire',
            'resume': u'Page vues, 15 derniers jours',
            'query': {
                'ids': 'ga:%s' % view_id,
                'start-date': '15daysAgo',
                'end-date': 'yesterday',
                'metrics': 'ga:pageviews',
                'dimensions': 'ga:pagePath',
                'sort': '-ga:pageviews',
                'max-results': 7
            },
                'chart': {
                'type': 'PIE',
                'options': {
                    'pieHole': 4/9,
                 }
            }
        },
        {
            'title': u'Navigateurs',
            'resume': u'15 derniers jours',
            'query': {
                'ids': 'ga:%s' % view_id,
                'start-date': '15daysAgo',
                'end-date': 'yesterday',
                'metrics': 'ga:sessions',
                'dimensions': 'ga:browser',
                'sort': '-ga:sessions',
                'max-results': 7
            },
                'chart': {
                'type': 'PIE',
                'options': {
                    'pieHole': 4/9,
                }
            }
        },
        {
            'title': u'Acquisition',
            'resume': u'Trafic d\'orientation, 15 derniers jours',
            'query': {
                'ids': 'ga:%s' % view_id,
                'start-date': '15daysAgo',
                'end-date': 'yesterday',
                'metrics': 'ga:sessions',
                'dimensions': 'ga:source',
                'sort': '-ga:sessions',
                'max-results': 7
            },
            'chart': {
                'container': 'chart-4-container',
                'type': 'PIE',
                'options': {
                'pieHole': 4/9,
                }
            }
        },
        {
            'title': u'Audience',
            'resume': u'Pays, 15 derniers jours',
            'query': {
                'ids': 'ga:%s' % view_id,
                'start-date': '15daysAgo',
                'end-date': 'yesterday',
                'metrics': 'ga:sessions',
                'dimensions': 'ga:country',
                'sort': '-ga:sessions',
                'max-results': 7
            },
            'chart': {
                'container': 'chart-5-container',
                'type': 'PIE',
                'options': {
                    'pieHole': 4/9,
                }
            }
        },
        {
            'title': u'Social',
            'resume': u'Interactions, 15 derniers jours',
            'query': {
                'ids': 'ga:%s' % view_id,
                'start-date': '15daysAgo',
                'end-date': 'yesterday',
                'metrics': 'ga:socialInteractions',
                'dimensions': 'ga:socialInteractionNetwork',
                'sort': '-ga:socialInteractions',
                'max-results': 7
            },
            'chart': {
                'container': 'chart-6-container',
                'type': 'PIE',
                'options': {
                    'pieHole': 4/9,
                }
            }
        },
    ]

    return {
        'token': token,
        'view_id': view_id,
        'charts': charts,
    }
