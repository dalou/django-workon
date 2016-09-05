# encoding: utf-8

import unicodedata
from django.utils.encoding import force_str, force_text
from django.utils.text import slugify as django_slugify

def forceunicode(string):
    enc = 'utf-8'
    try: return string.decode(enc)
    except:
        enc = 'ISO-8859-1'
        try: return string.decode(enc)
        except:
            enc = 'ascii'
            try: return string.decode(enc)
            except: return string
    return string

def normalize(string):
    if not string: return ""
    if not type(string) == type(unicode): string = forceunicode(string)
    string = string.replace(u'“', '"')
    string = string.replace(u'”', '"')
    string = string.replace(u'’', "'")
    string = string.replace(u'–', "-")
    return unicodedata.normalize('NFKD',string).encode('ascii','ignore').lower().strip()


def normalize_hard(string):
    if not string: return ""
    if not type(string) == type(unicode): string = forceunicode(string)
    string = normalize(string)
    string = string.replace(u'"', '')
    string = string.replace(u"'", '')
    string = string.replace(u'-', '')
    return unicodedata.normalize('NFKD',string).encode('ascii','ignore').lower().strip()

def slugify(string, allow_unicode=False):
    return django_slugify(string)