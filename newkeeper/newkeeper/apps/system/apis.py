# -*- coding: utf-8 -*-
"""
System status API
"""

__copyright__ = """ Copyright (c) 2022 newkeeper.org. All rights reserved."""
__version__ = '$Rev$'
__author__ = 'yanhang@diynova.com'

import logging
from utils import http

logger = logging.getLogger(__name__)


# API functions
def api_ping(request, version):
    return http.JsonSuccessResponse()


def api_get_ip(request, version):
    ip = http.get_client_ip(request)
    return http.JsonSuccessResponse({'ip': ip})


def api_show_version(request, version):
    """Show the api version for uri: /version
    """
    return http.JsonSuccessResponse({'version': version})
