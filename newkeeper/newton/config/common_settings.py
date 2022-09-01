# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """  """

from enum import Enum
from config import codes
from config.server import *

# Proxy settings
USE_X_FORWARDED_HOST = True

# User Default Preferred Language Code
USER_DEFAULT_LANGUAGE_CODE = 'en-us'


CHAIN_NAMES = {
    1002: 'Newton Devnet',
    1007: 'Newton Testnet',
    1012: 'Newton',
}

ACTIVITY_EVENT_CHOICES = (
    ("MINTED", "MINTED"),
    ("LIST", "LIST"),
    ("BID", "BID"),
    ("SALE", "SALE"),
    ("TRANSFER", "TRANSFER"),
)

ACTIVITY_EVENT_NAMES = {
    "MINTED": "Mint",
    "LIST": "List",
    "BID": "Bid",
    "SALE": "Sale",
    "TRANSFER": "Transfer",
}
