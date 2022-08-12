# -*- coding: utf-8 -*-
"""
User functional data processing.
"""

__copyright__ = """ Copyright (c) 2022 Newton Foundation. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

import json
import logging
import os
import requests
import shutil
import hashlib
from django.conf import settings

from utils import newchain_tools, newton_web3
from . import models as key_models

logger = logging.getLogger(__name__)


def check_owner(hex_address, contract_address, token_id):
    try:
        token_id = int(token_id)
        w3 = newton_web3.get_web3()
        chain_id = int(w3.net.version)
        w3.eth.account.chain_id = chain_id
        f = open("contracts/EVTEncryption.json")
        key_abi = json.load(f)
        f.close()
        encryption = w3.eth.contract(address=w3.toChecksumAddress(contract_address), abi=key_abi)
        owner_address = encryption.functions.ownerOf(token_id).call()

        if owner_address.lower() == hex_address.lower():
            return True
        else:
            return False
    except Exception as e:
        logger.exception("failed to check owner: %s" % str(e))
        return False
