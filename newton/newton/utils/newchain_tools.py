# -*- coding: utf-8 -*-
"""
Cryptography, address, transaction manipulation for newchain.
"""
__copyright__ = """ Copyright (c) 2022 Newton Foundation. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

import binascii
import json
import logging
from decimal import Decimal

import base58
from django.conf import settings
import rlp
from eth_typing import HexStr
from rlp.sedes import big_endian_int, binary, Binary
from sha3 import keccak_256
from web3 import Web3
from web3.middleware import geth_poa_middleware
# from ethereum import keys

logger = logging.getLogger(__name__)


class Transaction(rlp.Serializable):

    """
    Copy from ethereum.Transaction
    A transaction is stored as:
    [nonce, gasprice, startgas, to, value, data, v, r, s]

    nonce is the number of transactions already sent by that account, encoded
    in binary form (eg.  0 -> '', 7 -> '\x07', 1000 -> '\x03\xd8').

    (v,r,s) is the raw Electrum-style signature of the transaction without the
    signature made with the private key corresponding to the sending account,
    with 0 <= v <= 3. From an Electrum-style signature (65 bytes) it is
    possible to extract the public key, and thereby the address, directly.

    A valid transaction is one where:
    (i) the signature is well-formed (ie. 0 <= v <= 3, 0 <= r < P, 0 <= s < N,
        0 <= r < P - N if v >= 2), and
    (ii) the sending account has enough funds to pay the fee and the value.
    """
    address = Binary.fixed_length(20, allow_empty=True)
    fields = [
        ('nonce', big_endian_int),
        ('gasprice', big_endian_int),
        ('startgas', big_endian_int),
        ('to', address),
        ('value', big_endian_int),
        ('data', binary),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int),
    ]


chainID = settings.CHAIN_ID
PREFIX = 'NEW'


def address_encode(address_data):
    logger.debug('Entry the function address_encode.')
    if address_data.startswith('0x'):
        address_data = address_data[2:]
    hex_chainID = hex(chainID)[2:][-8:]
    if (len(hex_chainID) % 2) == 1:
        hex_chainID = '0' + hex_chainID
    num_sum = hex_chainID + address_data
    data = base58.b58encode_check(b'\0' + binascii.a2b_hex(num_sum))
    new_address = PREFIX + data.decode()
    return new_address

def newid_encode_by_public_key(public_key):
    if public_key.startswith('0x'):
        public_key = public_key[2:]
    if len(public_key) < 64:
        public_key = '0' * (64 - len(public_key)) + public_key
    k = keccak_256()
    k.update(bytearray.fromhex(public_key))
    data = k.hexdigest()
    hex_chainID = hex(chainID)[2:][-8:]
    if (len(hex_chainID) % 2) == 1:
        hex_chainID = '0' + hex_chainID
    num_sum = hex_chainID + data
    data = base58.b58encode_check(b'\0' + binascii.a2b_hex(num_sum))
    newid = PREFIX + 'ID' + data.decode()
    return newid

def newid_encode(address):
    if address.startswith('0x'):
        address = address[2:]
    hex_chainID = hex(chainID)[2:][-8:]
    if (len(hex_chainID) % 2) == 1:
        hex_chainID = '0' + hex_chainID
    num_sum = hex_chainID + address
    data = base58.b58encode_check(b'\0' + binascii.a2b_hex(num_sum))
    newid = PREFIX + 'ID' + data.decode()
    return newid

def b58check_decode(new_address):
    """ Decoding function """
    try:
        if new_address.startswith(PREFIX):
            new_address = base58.b58decode_check(new_address[3:])
            address_data = '0x' + binascii.b2a_hex(new_address).decode()[6:]
            return address_data
        if new_address.startswith('0x'):
            return new_address
    except Exception as e:
        logger.error("b58check_decode error for newaddress: %s error: %s" % (new_address, str(e)))
        return None

def newid_decode(newid):
    """ NewID decoding function """
    data = base58.b58decode_check(newid[5:])
    address_data = '0x' + binascii.b2a_hex(data).decode()[6:]
    return address_data


def generate_address_by_public_key(public_key):
    """ Generate address by public key"""
    k = keccak_256()
    if public_key.startswith('0x'):
        public_key = public_key[2:]
    k.update(bytearray.fromhex(public_key))
    data = k.hexdigest()
    address = data[len(data)-40:]
    new_address = address_encode(address)
    return new_address


def new_to_hex(new_address):
    return new_address_to_hex_address(new_address)


def new_address_to_hex_address(new_address):
    return "0x%s" % base58.b58decode_check(new_address[3:]).hex().lower()[6:]


def send_raw_transaction(raw, rpc_url=settings.NEWCHAIN_RPC_URL, wait_mining=False):
    """Send the raw transaction
    :param string raw: raw transaction
    :return: transaction id
    :rtype: string
    """
    try:
        provider = Web3.HTTPProvider(rpc_url)
        w3 = Web3(provider)
        txid = w3.eth.sendRawTransaction(raw)
        if wait_mining:
            w3.eth.waitForTransactionReceipt(txid)
        logger.info("txid:%s" % txid.hex())
        return txid.hex()
    except Exception as e:
        logger.exception('fail to send raw transaction:%s' % str(e))
        return ''


def check_transaction_status(txid: HexStr, rpc_url=settings.NEWCHAIN_RPC_URL):
    """ Check transaction status
    :param string txid: transaction hash
    :return: transaction id
    :rtype: string
    """
    try:
        provider = Web3.HTTPProvider(rpc_url)
        w3 = Web3(provider)
        receipt = w3.eth.waitForTransactionReceipt(txid)
        return receipt.status == 1
    except Exception as e:
        logger.exception('check_transaction_status error:%s' % str(e))
        return False


def get_transaction_receipt(txid, rpc_url=settings.NEWCHAIN_RPC_URL):
    """Get the receipt of transaction
    :param string txid:  transaction id
    :return: status
    :rtype: bool
    """
    try:
        provider = Web3.HTTPProvider(rpc_url)
        w3 = Web3(provider)
        response = w3.eth.getTransactionReceipt(txid)
        logger.info("response:%s" % response)
        return True
    except Exception as e:
        logger.exception('fail to get the transaction receipt:%s' % str(e))
        return False


def get_public_key_by_newid_contract(unencoded_newid, rpc_url=settings.NEWCHAIN_RPC_URL):
    """Query the public key by given newid in onchain contract
    :param string unencoded_newid:  unencoded newid 
    :return: public key
    :rtype: string
    """
    try:
        identity = unencoded_newid
        provider = Web3.HTTPProvider(rpc_url)
        w3 = Web3(provider)
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        f = open("contracts/UserRegistry.json")
        info_json = json.load(f)
        user_registry_abi = info_json["abi"]
        f.close()
        f = open("contracts/ClaimHolder.json")
        info_json = json.load(f)
        claim_holder_abi = info_json["abi"]
        f.close()
        # call registry
        contract_address = w3.toChecksumAddress(b58check_decode(settings.NEWID_CONTRACT_ADDRESS))
        newid_registry_contract = w3.eth.contract(address=contract_address, abi=user_registry_abi)
        bytes_identity = w3.toBytes(hexstr=identity)
        claim_holder_contract_address = newid_registry_contract.functions.identityRelations(bytes_identity).call()
        logger.info("claim_holder_contract_address:%s" % claim_holder_contract_address)
        # call claim holder
        newid_registry_contract = w3.eth.contract(address=claim_holder_contract_address, abi=claim_holder_abi)
        public_key = '0x' + newid_registry_contract.functions.getPublicKey().call().hex()
        logger.info("public_key:%s" % public_key)
        return public_key
    except Exception as e:
        logger.exception('fail to get the public key from the newid contract:%s' % str(e))
        return ''


def send_raw_transaction_dummy(raw, rpc_url=settings.NEWCHAIN_RPC_URL):
    """Send the dummy raw transaction, only for unit testing 
    :param string raw: raw transaction
    :return: transaction id
    :rtype: string
    """
    import random
    return '0x09cb88c164c79d61b3e17470f633c556dc5d42d13c2368b83dedd27584%s' % random.randint(100000,999999)


def add_bigint(a, b):
    """Add operation for bigint 
    :param string a: a
    :param string b: b
    :return: sum string
    :rtype: string
    """
    return str(Decimal(a) + Decimal(b))


def parse_raw_transaction(raw_transaction):
    """Parse raw transaction
    :param string raw_transaction: hex raw transaction
    :return: transaction dictionary
    :rtype: dict
    """
    try:
        if raw_transaction.startswith("0x"):
            raw_transaction = raw_transaction[2:]
        raw_transaction_bytes = bytearray.fromhex(raw_transaction)
        rlp_transaction = rlp.decode(Web3.toBytes(raw_transaction_bytes), Transaction)
        to = binascii.hexlify(rlp_transaction.to)
        value = rlp_transaction.value
        return {
            'to': '0x' + to.decode('ascii').lower(),
            'value': value,
            'data': '0x' + rlp_transaction.data.hex()
        }
    except Exception as e:
        logger.exception('fail to parse raw transaction:%s' % str(e))
        return None



if __name__ == "__main__":
    address_data = '0xBBaC0fEBD7F42aC11BCE39e2f49A5EfbA73899B6'
    new_address = address_encode(address_data)
    print(new_address)
    decode_result = b58check_decode('NEW132AYrd4F2jVXhUddYJqT16KRN8LYN3MCHRie')
    print(decode_result)
    #print(parse_raw_transaction('0xf86a0a6483015f909414aa5732a2833143e8a552307137122a7b83954e880de0b6b3a7640000808207f8a0a498d321d46a02e6420328ac3408b42e0a2ae0dea136d1fb628f8372cc2cb535a006ff7b94e0ade5068d44c7550d7008871c02d610715d5d4726b6cec5b1e7fbbf'))
