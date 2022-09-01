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
