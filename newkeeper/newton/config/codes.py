# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """  """

from enum import Enum


class ErrorCode(Enum):
    FAIL = 0
    SUCCESS = 1
    UNAUTH = 2
    SIGN_ERROR = 3
    INVALID_PARAMS = 4
    MAINTAIN = 5
    UPGRADE = 6
    BLOCK_USER = 7
    TIMESTAMP_VERIFY_FAILED = 8
    TIMESTAMP_IS_EMPTY = 9


class Language(Enum):
    CHINESE = 1
    ENGLISH = 2


class SystemServiceStatus(Enum):
    MAINTAIN = 0
    NORMAL = 1


class StatusCode(Enum):
    INVALID = 0
    AVAILABLE = 1


class OrderBy(Enum):
    ASC = 0
    DESC = 1


class AppPlatform(Enum):
    IOS = 1
    ANDROID = 2
    IOS_ADHOC = 3
    DEVELOPER = 4
