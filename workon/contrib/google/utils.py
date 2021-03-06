import json

from django.conf import settings
from django import template
try:
    from raven.contrib.django.raven_compat.models import client as raven
except:
    raven = None
try:

    from oauth2client.service_account import ServiceAccountCredentials

    def get_google_account_token(account_key_file):
        # The scope for the OAuth2 request.
        SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
        token = None
        try:
            _key_data = json.load(account_key_file)
            _credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                _key_data,
                scopes=['https://www.googleapis.com/auth/analytics.readonly'],
                # token_uri='https://accounts.google.com/o/oauth2/token'
            )
            token = _credentials.get_access_token().access_token
        except Exception, e:
            if raven:
                raven.captureException()
            print "GOOGLE API TOKEN RETRIEVE ERROR:", e.message
            token = None
        return token

except:

    from oauth2client.client import SignedJwtAssertionCredentials

    def get_google_account_token(account_key_file):
        # The scope for the OAuth2 request.
        SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
        token = None
        try:
            _key_data = json.load(account_key_file)
            _credentials = SignedJwtAssertionCredentials(
                _key_data['client_email'],
                _key_data['private_key'],
                'https://www.googleapis.com/auth/analytics.readonly',
                # token_uri='https://accounts.google.com/o/oauth2/token'
            )
            token = _credentials.get_access_token().access_token
        except Exception, e:
            if raven:
                raven.captureException()
            print "GOOGLE API TOKEN RETRIEVE ERROR:", e.message
            token = None
        return token