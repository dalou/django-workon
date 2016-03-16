# encoding: utf-8

import unicodedata
from django.utils.encoding import force_str, force_text

def forceunicode(str):
    enc = 'utf-8'
    try: return str.decode(enc)
    except:
        enc = 'ISO-8859-1'
        try: return str.decode(enc)
        except:
            enc = 'ascii'
            try: return str.decode(enc)
            except: return str
    return str

def normalize(str):
    if not str: return ""
    str = str.replace(u'’', "'")
    if not type(str) == type(unicode): str = forceunicode(str)
    return unicodedata.normalize('NFKD',str).encode('ascii','ignore').lower().strip()

