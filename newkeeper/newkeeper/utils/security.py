# -*- coding: utf-8 -*-
"""
Encrypt and decode.
"""

__copyright__ = """ Copyright (c) 2022 newkeeper.org. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

from email.mime import base
import re
import sys
import random
import uuid
import hashlib
import urllib
import collections
import importlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from Crypto import Random
from django.conf import settings
from Crypto.Cipher import AES

'''
AES ENCRYPT
'''

def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)

# AES ENCRYPT
def aes_encrypt(key, text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    encrypt_aes = aes.encrypt(add_to_16(text))
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
    return encrypted_text

# AES DECRYPT
def aes_decrypt(key, text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
    return decrypted_text


def generate_uuid():
    return str(uuid.uuid4().hex)


def generate_digest(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def generate_digest_for_file(filename, block_size=2**20):
    md5 = hashlib.md5()
    f = open(filename)
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()


def sign_hmac(data, secret, prefix='', use_urlencode=False, joint='&'):
    data = collections.OrderedDict(sorted(data.items()))
    sign_string = prefix
    n = 0
    for k, v in data.items():
        if n != 0 and k != 'sign':
            sign_string += joint
        n += 1
        if k != 'sign':
            sign_string += u'%s=%s' % (k, v)
    sign_string += secret
    if use_urlencode:
        sign_string = urllib.quote_plus(sign_string)
    signed_string = generate_digest(sign_string)
    return signed_string


def generate_verify_code():
    """ Generate the 6-number verify code 
    """
    code = random.randint(100000, 999999)
    return code


def rsa_verify(data, pub_key, sign):
    key = RSA.importKey(pub_key)
    h = SHA.new(data)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, base64.b64decode(sign)):
        return True
    return False


def generate_digest_sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    res = sha256.hexdigest()
    return res


def openapi_sign_hmac(request_meta, data, secret, use_urlencode=False, joint='&'):
    request_host = request_meta.get('HTTP_HOST')
    request_url = request_meta.get("PATH_INFO")
    request_method = request_meta.get('REQUEST_METHOD')
    sign_string = '%s\n%s\n%s\n' % (request_method, request_host, request_url)
    data = collections.OrderedDict(sorted(data.items()))
    n = 0
    for k, v in data.items():
        if n != 0 and k != 'Signature':
            sign_string += joint
        n += 1
        if k != 'Signature':
            sign_string += u'%s=%s' % (k, v)
    sign_string += secret
    if use_urlencode:
        sign_string = urllib.parse.quote_plus(sign_string)
    signed_string = generate_digest_sha256(sign_string)
    signed_string = base64.b64encode(sign_string.encode('utf-8'))
    return str(signed_string,'utf-8')
