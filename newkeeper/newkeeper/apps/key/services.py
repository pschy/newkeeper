# -*- coding: utf-8 -*-
"""
User functional data processing.
"""

__copyright__ = """ Copyright (c) 2022 newkeeper.org. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

import json
import logging
from django.conf import settings
from utils import newton_web3

logger = logging.getLogger(__name__)


def check_permission(w3, hex_address, key_id, token_id, rpc_url, nft_contract, evt_contract):
    try:
        if not w3:
            return False, 'chainId error'

        token_id = int(token_id)
        hex_address = hex_address.lower()

        nft_balance = newton_web3.get_contracts_balance(w3, rpc_url, hex_address, nft_contract)
        if int(nft_balance) <= 0:
            return False, 'nft balance error'

        result = newton_web3.has_permission(w3, rpc_url, hex_address, token_id, key_id, evt_contract)
        if not result:
            return False, 'permission error'

        return True, ''
    except Exception as e:
        logger.exception("failed to check permission: %s" % str(e))
        return False, 'failed to check permission'
