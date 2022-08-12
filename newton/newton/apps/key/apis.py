# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2022 Newton Foundation. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

import logging
from utils import http
from django.conf import settings
import os
import json
from . import forms as key_forms
from . import models as key_models
from . import services as key_services
from django.http import HttpResponseNotFound
from eth_account.messages import encode_defunct, encode_structured_data
from utils import newton_web3
from utils import ecc_tools, newchain_tools, security
from openid.dh import DiffieHellman
from openid.constants import DEFAULT_DH_GENERATOR
from openid import cryptutil


logger = logging.getLogger(__name__)


def api_generator(request, version):
    try:
        form = key_forms.GeneratorForm(request.POST)
        if not form.is_valid():
            logger.error('validate error:%s' % form.errors)
            return http.JsonErrorResponse(error_message='validate error')
        prime = form.cleaned_data["prime"]
        peer_public_key = form.cleaned_data["peer_public_key"]

        dh_node = DiffieHellman(prime, DEFAULT_DH_GENERATOR)
        node_public_key = dh_node.public_key
        shared_secret = dh_node.getSharedSecret(peer_public_key)
        node_secret = hex(shared_secret)

        key_id = security.generate_digest_sha256(peer_public_key)
        key_obj = key_models.KeyList.objects.filter(key_id=key_id).first()
        if not key_obj:
            key_models.KeyList.objects.create(
                key_id=key_id,
                encrypt_key=node_secret
            )
        else:
            return http.JsonErrorResponse(error_message='key already exist')

        data = {
            "node_public_key": node_public_key,
        }
        return http.JsonSuccessResponse(data=data)
    except Exception as e:
        logger.exception("fail to generator: %s" % str(e))
        return http.JsonErrorResponse()


def api_bind(request, version):
    try:
        form = key_forms.BindForm(request.POST)
        if not form.is_valid():
            logger.error('validate error:%s' % form.errors)
            return http.JsonErrorResponse(error_message='validate error')
        key_id = form.cleaned_data["key_id"]
        contract_address = form.cleaned_data["contract_address"]
        token_id = form.cleaned_data["token_id"]
        chain_id = settings.CHAIN_ID if not form.cleaned_data["chain_id"] else form.cleaned_data["chain_id"]
        private_key = form.cleaned_data["private_key"]
        sign_r = form.cleaned_data["sign_r"]
        sign_s = form.cleaned_data["sign_s"]
        sign_v = form.cleaned_data["sign_v"]
        sign_message = form.cleaned_data["sign_message"]

        key_obj = key_models.KeyList.objects.filter(key_id=key_id).first()
        if not key_obj:
            return http.JsonErrorResponse(error_message='key is not exist')
        encrypt_key = security.aes_decrypt(key_obj.encrypt_key[2:32], private_key)

        sign_message = json.loads(sign_message)
        sign_message = encode_structured_data(primitive=sign_message)
        w3 = newton_web3.get_web3()
        vrs = (sign_v, sign_r, sign_s)
        hex_address = w3.eth.account.recover_message(sign_message, vrs=vrs)
        if not hex_address:
            return http.JsonErrorResponse(error_message='recover message error')

        res = key_services.check_owner(hex_address, contract_address, token_id)
        if not res:
            return http.JsonErrorResponse(error_message='check owner failed')

        key_obj.contract_address = contract_address.lower()
        key_obj.token_id = str(token_id)
        key_obj.chain_id = chain_id
        key_obj.encrypt_key = encrypt_key
        key_obj.bind_status = 1
        key_obj.save()

        return http.JsonSuccessResponse()
    except Exception as e:
        logger.exception("fail to check: %s" % str(e))
        return http.JsonErrorResponse()


def api_get(request, version, symbol):
    try:
        form = key_forms.CheckForm(request.POST)
        if not form.is_valid():
            logger.error('validate error:%s' % form.errors)
            return http.JsonErrorResponse(error_message='validate error')

        key_id = form.cleaned_data["key_id"]
        prime = form.cleaned_data["prime"]
        peer_public_key = form.cleaned_data["peer_public_key"]
        sign_r = form.cleaned_data["sign_r"]
        sign_s = form.cleaned_data["sign_s"]
        sign_v = form.cleaned_data["sign_v"]
        sign_message = form.cleaned_data["sign_message"]

        key_obj = key_models.KeyList.objects.filter(key_id=key_id).first()
        if not key_obj:
            return http.JsonErrorResponse(error_message='key is not exist')

        sign_message = json.loads(sign_message)
        sign_message = encode_structured_data(primitive=sign_message)
        w3 = newton_web3.get_web3()
        vrs = (sign_v, sign_r, sign_s)
        hex_address = w3.eth.account.recover_message(sign_message, vrs=vrs)
        if not hex_address:
            return http.JsonErrorResponse(error_message='recover message error')

        res = key_services.check_owner(hex_address, contract_address, token_id)
        if not res:
            return http.JsonErrorResponse(error_message='check failed')

        dh_node = DiffieHellman(prime, DEFAULT_DH_GENERATOR)
        node_public_key = dh_node.public_key
        shared_secret = dh_node.getSharedSecret(peer_public_key)
        node_secret = hex(shared_secret)

        data = {
            'node_public_key': node_public_key,
            'private_key': security.aes_encrypt(node_secret[2:32], key_obj.encrypt_key)
        }

        return http.JsonSuccessResponse(data=data)
    except Exception as e:
        logger.exception("fail to check: %s" % str(e))
        return http.JsonErrorResponse()
