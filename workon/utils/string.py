# encoding: utf-8

import unicodedata, re, json

from django.utils.encoding import force_str, force_text
from django.utils.text import slugify as django_slugify

from unidecode import unidecode

# space_chars = re.compile(r"[\.\'\"\_\-\,\?\(\)\[\]]")

__all__ = [
    "forceunicode",
    "normalize",
    "normalize_hard",
    "slugify",
    "prepare_for_search",
    "jsonify",
]

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

def jsonify(obj):
    if obj is None:
        return "{}"
    if isinstance(obj,dict):
        return json.dumps(obj)
    elif isinstance(obj,list):
        return json.dumps(obj)
    else:
        obj = re.sub(r'([\w\d_]+)\:', '"\\1":', obj)
        obj = re.sub(r'\'', '"', obj)
        obj = re.sub(r'\/\/\s*[\w\s\d]+', '', obj)
        obj = re.sub(r'Date\.UTC\(.+\)', '""', obj)

        try:
            return json.dumps(json.loads(obj))
        except:
            return json.loads(json.dumps(obj))

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

def prepare_for_search(string, default=""):
    if not string: return default
    if not type(string) == type(unicode): string = forceunicode(string)
    string = string.replace(u'“', ' ')
    string = string.replace(u'”', ' ')
    string = string.replace(u'"', ' ')
    string = string.replace(u"'", ' ')
    string = string.replace(u'’', " ")
    string = string.replace(u'–', " ")
    string = string.replace(u'_', " ")
    return unidecode(slugify(string).replace('-', ' ')).lower().strip()