# -*- coding: utf-8 -*-
"""
User functional data processing.
"""

__copyright__ = """ Copyright (c) 2022 newkeeper.org. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

import logging
from django.conf import settings
import rlp
from rlp.sedes import big_endian_int, binary, Binary

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
        rlp_data = rlp.decode(bytes.fromhex(sign_data[2:]), BindParams)
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
        rlp_data = rlp.decode(bytes.fromhex(sign_data[2:]), GetParams)
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
