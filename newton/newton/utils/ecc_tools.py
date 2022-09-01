# -*- coding: utf-8 -*-
"""
Verify Signature.
"""

__copyright__ = """ Copyright (c) 2022 newkeeper.org. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'chenpengtao@diynova.com'

import logging
from fastecdsa import curve, ecdsa, keys
from sha3 import keccak_256
from django.conf import settings

logger = logging.getLogger(__name__)


def validate_p256_signature(r, s, m, validate_public_keys):
    """Validate the p256 signature

    :param string r: r part of signature
    :param string s: s part of signature
    :param string m: message for signature
    :param list validate_public_keys: public key list for validation
    :return: True if it is valid signature, otherwise False    
    """
    try:
        public_key_list = extract_public_key_list(r, s, m)
        logger.debug("public_key_list:%s, validate_public_keys:%s" % (public_key_list, validate_public_keys))
        for public_key in public_key_list:
            if public_key in validate_public_keys:
                return True
        return False
    except Exception as e:
        logger.exception('Failed to validate the p256 signature:%s' % str(e))
        return False

def extract_public_key_list(r, s, m):
    try:
        public_key_point = keys.get_public_keys_from_sig((int(r, 16), int(s, 16)), m, curve.P256, hashfunc=keccak_256)
        public_key_list = []
        for i in public_key_point:
            x = str(hex(i.x)[2:])
            y = str(hex(i.y)[2:])
            if len(x) < 64:
                x = '0' * (64 - len(x)) + x
            if len(y) < 64:
                y = '0' * (64 - len(y)) + y
            public_key = '0x' + x + y
            public_key_list.append(public_key)
        return public_key_list
    except Exception as e:
        logger.exception('Failed to extract the public key list:%s' % str(e))
        return []


def generate_p256_key_pairs():
    private_key, public_key = keys.gen_keypair(curve.P256)
    print(private_key)
    print()
    print(public_key)
    private_key = str(hex(private_key))
    x = str(hex(public_key.x))[2:]
    y = str(hex(public_key.y))[2:]
    if len(x) < 64:
        x = '0' * (64 - len(x)) + x
    if len(y) < 64:
        y = '0' * (64 - len(y)) + y
    public_key =  '0x' + x + y
    if len(private_key) < 66:
        private_key = '0x' + '0' * (66 - len(private_key)) + private_key[2:]
        logger.info("convert the private key which length is 63 ")
    return private_key, public_key


def sign_p256(message, private_key, hashfunc=keccak_256):
    r, s = ecdsa.sign(message, private_key, hashfunc=hashfunc)
    return str(hex(r)), str(hex(s))

def concat_signature(r, s):
    if r.startswith('0x'):
        r = r[2:]
    if len(r) < 64:
        r = '0' * (64 - len(r)) + r
    if s.startswith('0x'):
        s = s[2:]
    if len(s) < 64:
        s = '0' * (64 - len(s)) + s    
    return '0x' + r + s

def load_private_key(path):
    out = keys.import_key(path)
    p = out[1]
    x = str(hex(p.x))[2:]
    y = str(hex(p.y))[2:]
    if len(x) < 64:
        x = '0' * (64 - len(x)) + x
    if len(y) < 64:
        y = '0' * (64 - len(y)) + y
    p =  '0x' + x + y
    return out[0], p
