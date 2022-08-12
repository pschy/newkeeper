# -*- coding: utf-8 -*-
"""
Django settings for lubangame  project.

"""
from config import codes

# message content
from django.utils.translation import gettext_lazy as _

# Error message
ERROR_CODE_LABEL = {
    codes.ErrorCode.FAIL.value: _('Operation failed'),
    codes.ErrorCode.SUCCESS.value: _('Operation success'),
    codes.ErrorCode.UNAUTH.value: _('Session unavailable, please login!'),
    codes.ErrorCode.BLOCK_USER.value: _('Account exceptions, please contact the administrator!'),
    codes.ErrorCode.SIGN_ERROR.value: _('Signature error'),
    codes.ErrorCode.INVALID_PARAMS.value: _('Parameters error'),
    codes.ErrorCode.UPGRADE.value: _('Your app version is too old, please upgrade'),
}
