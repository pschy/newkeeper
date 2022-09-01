# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2022 newkeeper.org. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'


import logging
import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class ProcessSessionMiddleware(MiddlewareMixin):
    """Process session"""
    def process_request(self, request):
        logger.info("received request post utl: %s" % str(request.META.get("PATH_INFO")))
        logger.info("received request post data: %s" % str(request.POST))
