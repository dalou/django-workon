# encoding: utf-8

import hashlib, random, base64

from Crypto.Cipher import AES
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import base36_to_int, int_to_base36

__all__ = ["random_token", "base64_crypted_key", "base64_decrypted_key", "request_uid_token"]

def random_token(extra=None, hash_func=hashlib.sha256):
    if extra is None:
        extra = []
    elif not isinstance(extra, list) or not isinstance(extra, tuple):
        extra = [str(extra)]
    bits = [ str(e) for e in extra ] + [str(random.SystemRandom().getrandbits(512))]
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


def request_uid_token(request):
    uid = int_to_base36(request.user.id)
    token = default_token_generator.make_token(request.user)
    return uid, token

