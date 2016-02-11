
# encoding: utf-8

import datetime
import operator
import hashlib
import random
import functools
from Crypto.Cipher import AES
import base64

def random_token(extra=None, hash_func=hashlib.sha256):
    if extra is None:
        extra = []
    print extra
    bits = extra + [str(random.SystemRandom().getrandbits(512))]
    return hash_func("".join(bits)).hexdigest()


def base64_crypted_key(string, passphrase=''):
    try:
        string = (( '%s|'% (string)) * 32)[0:32]
        secret_key = passphrase.rjust(12)
        cipher = AES.new(secret_key,AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(string))
    except:
        return None


def base64_decrypted_key(string, passphrase=''):
    try:
        secret_key = passphrase.rjust(12)
        cipher = AES.new(secret_key,AES.MODE_ECB)
        decoded = cipher.decrypt(base64.b64decode(string))
        print decoded
        return decoded.strip().split('|')[0]
    except:
        return None


