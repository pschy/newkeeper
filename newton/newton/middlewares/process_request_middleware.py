# -*- coding: utf-8 -*-
"""
ProcessRequestMiddleware
"""

__copyright__ = """ Copyright (c) 2022 Newton Foundation. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

import logging
import json
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class ProcessRequestMiddleware(MiddlewareMixin):
    """handle hmac sign from app"""
    def process_request(self, request):
        try:
            content_type = request.META.get('CONTENT_TYPE', "")
            if not content_type:
                content_type = request.META.get('HTTP_CONTENT_TYPE', "")
            if not request.POST and content_type.find('application/json') > -1:
                data = json.loads(request.body.decode('utf-8'))
                if data:
                    request.POST = data
            if not request.POST and settings.ENV_DEV == True and request.method == 'GET':
                request.POST = request.GET

            if settings.ENV_DEV == True:
                logger.info('received POST is %s.' % request.POST)

        except Exception as e:
            logger.exception("HmacSignMiddleware process request error: %s" % str(e))
