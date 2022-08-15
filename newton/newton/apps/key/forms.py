# -*- coding: utf-8 -*-
"""
Common form verification.
"""

__copyright__ = """ Copyright (c) 2022 Newton Foundation. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

from django import forms
from django.conf import settings


class GeneratorForm(forms.Form):
    prime = forms.CharField(required=True, max_length=512)
    peer_swap_key = forms.CharField(required=True, max_length=512)


class BindForm(forms.Form):
    key_id = forms.CharField(required=True, max_length=512)
    contract_address = forms.CharField(required=True, max_length=128)
    token_id = forms.CharField(required=True, max_length=64)
    chain_id = forms.CharField(required=False, max_length=64)
    private_key = forms.CharField(required=True, max_length=1024)
    sign_r = forms.CharField(required=True, max_length=66)
    sign_s = forms.CharField(required=True, max_length=66)
    sign_v = forms.CharField(required=True, max_length=66)
    sign_message = forms.CharField(required=True, max_length=2048)


class GetForm(forms.Form):
    key_id = forms.CharField(required=True, max_length=512)
    prime = forms.CharField(required=True, max_length=512)
    peer_swap_key = forms.CharField(required=True, max_length=512)
    sign_r = forms.CharField(required=True, max_length=66)
    sign_s = forms.CharField(required=True, max_length=66)
    sign_v = forms.CharField(required=True, max_length=66)
    sign_message = forms.CharField(required=True, max_length=2048)
