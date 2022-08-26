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
from utils import newton_web3
import rlp
from rlp.sedes import big_endian_int, binary, Binary
from web3 import Web3

logger = logging.getLogger(__name__)


class BindParams(rlp.Serializable):
    address = Binary.fixed_length(20, allow_empty=True)
    fields = [
        ('key_id', binary),
        ('contract_address', binary),
        ('nft_contract_address', binary),
        ('token_id', big_endian_int),
        ('chain_id', big_endian_int),
        ('rpc_url', binary),
        ('private_key', binary),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int),
        ('message', binary),
    ]


class GetParams(rlp.Serializable):
    fields = [
        ('key_id', binary),
        ('prime', binary),
        ('peer_swap_key', binary),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int),
        ('message', binary),
    ]


def decode_bind_params(sign_data):
    try:
        rlp_data = rlp.decode(Web3.toBytes(hexstr=sign_data), BindParams)
        if not rlp_data:
            return None
        form_data = {
            'key_id': rlp_data.key_id.decode(),
            'contract_address': rlp_data.contract_address.decode(),
            'nft_contract_address': rlp_data.nft_contract_address.decode(),
            'token_id': rlp_data.token_id,
            'chain_id': rlp_data.chain_id,
            'rpc_url': rlp_data.rpc_url.decode(),
            'private_key': rlp_data.private_key.decode(),
            'sign_v': rlp_data.v,
            'sign_r': hex(rlp_data.r),
            'sign_s': hex(rlp_data.s),
            'sign_message': rlp_data.message.decode(),
        }
        return form_data
    except Exception as e:
        logger.exception("failed to decode bind params: %s" % str(e))
        return False


def decode_get_params(sign_data):
    try:
        rlp_data = rlp.decode(Web3.toBytes(hexstr=sign_data), GetParams)
        if not rlp_data:
            return None
        form_data = {
            'key_id': rlp_data.key_id.decode(),
            'prime': rlp_data.prime.decode(),
            'peer_swap_key': rlp_data.peer_swap_key.decode(),
            'sign_v': rlp_data.v,
            'sign_r': hex(rlp_data.r),
            'sign_s': hex(rlp_data.s),
            'sign_message': rlp_data.message.decode(),
        }
        return form_data
    except Exception as e:
        logger.exception("failed to decode get params: %s" % str(e))
        return False


def check_permission(hex_address, key_id, token_id, rpc_url, nft_contract, evt_contract):
    try:
        w3 = newton_web3.get_web3(rpc_url)
        if not w3:
            return False, 'chainId error'

        token_id = int(token_id)
        hex_address = hex_address.lower()

        nft_balance = newton_web3.get_contracts_balance(rpc_url, hex_address, nft_contract)
        if int(nft_balance) <= 0:
            return False, 'nft balance error'

        result = newton_web3.has_permission(rpc_url, hex_address, token_id, key_id, evt_contract)
        if not result:
            return False, 'permission error'

        return True, ''
    except Exception as e:
        logger.exception("failed to check permission: %s" % str(e))
        return False, 'failed to check permission'
