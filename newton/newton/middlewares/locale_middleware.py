"""
Locale Middlwares Implementation includeing POST parameter, HTTP Header, etc.

"""

__copyright__ = """ Copyright (c) 2022 Newton Foundation. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'newkeeper'

import logging

from django.utils import translation
from django.middleware import locale
from django.conf import settings

from utils import language_utils

logger = logging.getLogger(__name__)

class LocaleFromPostMiddleware(locale.LocaleMiddleware):
    """
    LocaleFromPostMiddleware: Set the current language code by language filed in POST parameters
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response_header = self.get_response(request)
        response = self.process_response(request, response_header)
        return response

    def process_request(self, request):
        # check the langage in cookie
        language = language_utils.detect_language(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        return response
