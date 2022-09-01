# -*- coding: utf-8 -*-
"""
Form validation decorator.
"""

__copyright__ = """ Copyright (c) 2022 newkeeper.org. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'xiawu@zeuux.org'

import logging
import json
import time
from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
# from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.utils import translation
from django.utils.translation import gettext as _
from urllib.parse import urlparse
from django.shortcuts import resolve_url
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.cache import cache

from utils import language_utils
from utils import security
from utils import http
from utils import ecc_tools
from utils import newchain_tools
from utils import captcha_service
from config import codes
from config.server import STATUS_INFO, APP_KEY_TO_SECRET

logger = logging.getLogger(__name__)


def http_post_required(func):
    def _decorator(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed('Only POST here')
        return func(request, *args, **kwargs)

    return _decorator


def http_get_required(func):
    def _decorator(request, *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed('Only GET here')
        return func(request, *args, **kwargs)
    return _decorator


def access_required(func):
    """ Sign verification.
    :param func:
    :return: response
    """
    def _decorator(request, *args, **kwargs):
        # clean session cache
        # check user from access_token
        request.session['current_user'] = None
        request.session['current_user_id'] = None

        try:
            # content_type = request.META.get('CONTENT_TYPE') or request.META.get['HTTP_CONTENT_TYPE']
            # if not request.POST and content_type == 'application/json':
            #     data = json.loads(request.body.decode('utf-8'))
            #     if data:
            #         request.POST = data
                    # detect language
            language = language_utils.detect_language(request)
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
        except:
            pass

        if settings.ENV_DEV == True and request.path != '/api/v1/sign/test/':
            response = func(request, *args, **kwargs)
            return response

        sign = request.POST.get('sign')
        app_key = request.POST.get('app_key')
        if app_key in APP_KEY_TO_SECRET:
            logger.debug('app_key verification passed')
            # Verify timestamp.
            timestamp = request.POST.get('timestamp')
            if timestamp:
                now_time = time.time()
                interval_time = now_time - float(timestamp)
                if interval_time > 300:
                    logger.error('The timestamp verify failed, interval time more than 300s.')
                    return http.JsonErrorResponse(
                        error_code=codes.ErrorCode.TIMESTAMP_VERIFY_FAILED.value,
                        error_message='The timestamp verify failed, interval time more than 300s.')
            else:
                logger.error('The timestamp is empty.')
                return http.JsonErrorResponse(
                    error_code=codes.ErrorCode.TIMESTAMP_IS_EMPTY.value,
                    error_message='The timestamp is empty.')

            # Verify sign.
            secret = APP_KEY_TO_SECRET[app_key]
            signed_string = security.sign_hmac(request.POST, secret=secret)
            logger.debug('Received sign:%s' % sign)
            logger.debug('The sign calculated by the server:%s' % signed_string)
            if sign == signed_string:
                if STATUS_INFO.get('status') == codes.SystemServiceStatus.MAINTAIN.value:
                    return http.JsonErrorResponse(codes.ErrorCode.MAINTAIN.value, error_message=(STATUS_INFO.get('msg')),
                                                  data={'m_time': STATUS_INFO.get('m_time')})
                response = func(request, *args, **kwargs)
                logger.debug('send response is %s.' % response.content)
                return response
            else:
                logger.error("Sign value verification failed !")
                return http.JsonErrorResponse(error_message=_('Sign value verification failed !'))
        else:
            logger.error('Failed to get app key.')
            return http.JsonErrorResponse(error_message='Failed to get app key.')
    return _decorator


def captcha_required(func):
    """Check the validation of captcha
    :param func:
    :return: response
    """
    def _decorator(request, version, *args, **kwargs):
        try:

            captcha_service_type = request.POST.get('captcha_service_type')
            captcha_ticket = request.POST.get('captcha_ticket')
            captcha_random = request.POST.get('captcha_random')
            os_type = request.POST.get('os')
            ip_address = http.get_client_ip(request)
            
            if not settings.DEBUG:
                
                if captcha_service_type not in ['google', 'tencent', 'tencent_cloud']:
                    return http.JsonErrorResponse(error_message=_('invalid captcha type'))

                if not captcha_service.is_valid_captcha(captcha_service_type,
                                                        captcha_ticket,
                                                        captcha_random,
                                                        os_type,
                                                        ip_address, version):
                    logger.error("invalid captcha")
                    return http.JsonErrorResponse(error_message=_('invalid captcha'))
            response = func(request, version, *args, **kwargs)
            return response
        except Exception as e:
            logger.exception('fail to check captcha:%s' % str(e))
            return http.JsonErrorResponse(error_message=_('captcha error'))
    return _decorator
