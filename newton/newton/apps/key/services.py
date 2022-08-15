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
        ('token_id', big_endian_int),
        ('chain_id', big_endian_int),
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
            'token_id': rlp_data.token_id,
            'chain_id': rlp_data.chain_id,
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


def check_permission(hex_address, key_id, token_id, chain_id):
    try:
        token_id = int(token_id)
        chain_id = int(chain_id)
        w3 = newton_web3.get_web3(chain_id)
        w3.eth.account.chain_id = chain_id
        if not w3:
            return False, 'chainId error'

        nft_contract_address = w3.toChecksumAddress(settings.NFT_CONTRACT_ADDRESS[chain_id])
        encryption_contract_address = w3.toChecksumAddress(settings.ENCRYPTION_CONTRACT_ADDRESS[chain_id])
        hex_address = w3.toChecksumAddress(hex_address)

        f = open("contracts/Nft.json")
        nft_abi = json.load(f)
        f.close()
        nftContract = w3.eth.contract(address=nft_contract_address, abi=nft_abi)
        nft_balance = nftContract.functions.balanceOf(hex_address).call()
        if int(nft_balance) <= 0:
            return False, 'nft balance error'

        f = open("contracts/Encryption.json")
        key_abi = json.load(f)
        f.close()
        encryptionContract = w3.eth.contract(address=encryption_contract_address, abi=key_abi)
        result = encryptionContract.functions.hasPermission(token_id, key_id, hex_address).call()
        if not result:
            return False, 'permission error'

        return True, ''
    except Exception as e:
        logger.exception("failed to check permission: %s" % str(e))
        return False, 'failed to check permission'
