# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """  """

import platform
from logging.handlers import SysLogHandler
from config import codes

BASE_URL = 'http://127.0.0.1:8000'

ENV_DEV = True
DOMAIN = '127.0.0.1'

# Cache
DEFAULT_CACHE_DB = 1
REDIS_CACHE_DB = DEFAULT_CACHE_DB
REDIS_CACHE_PASSWORD = ''
REDIS_CACHE_HOST = '127.0.0.1'
REDIS_CACHE_PORT = 6379
REDIS_CACHE_URL = 'redis://%s:%s' % (REDIS_CACHE_HOST, REDIS_CACHE_PORT)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "%s/%s" % (REDIS_CACHE_URL, DEFAULT_CACHE_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'newkeeper'
    },
}

CURRENT_NET = 'TestNet'
DEFAULT_CHAIN_ID = 1007
CHAIN_ID = [1007, 1012]
RPC_URL = {
    1007: "https://rpc1.newchain.newtonproject.org/",
    1012: ""
}
NFT_CONTRACT_ADDRESS = {
    1007: "0xFD1d4413030c39758Afd48b34b839BFe265FD9D9",
    1012: ""
}
ENCRYPTION_CONTRACT_ADDRESS = {
    1007: "0x66fE876AD7C00319aF3030D3736A6D921CDF744B",
    1012: ""
}

# Logging
system_string = platform.system()
if system_string == 'Linux':
    syslog_path = '/dev/log'
elif system_string == 'Darwin':
    syslog_path = '/var/run/syslog'
else:
    raise Exception('nonsupport platform!')

LOGGING_LEVEL = 'INFO'
LOGGING_LEVEL_SENTRY = 'ERROR'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s][%(msecs)03d] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'syslog': {
            'level': LOGGING_LEVEL,
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL2,
            'formatter': 'verbose',
            'address': syslog_path,
        },
        # 'sentry': {
        #     'level': LOGGING_LEVEL_SENTRY,
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        #     'tags': {'custom-tag': 'x'},
        # },
    },
    'loggers': {
        '': {
            'handlers': ['console', ],
            'level': LOGGING_LEVEL,
        },
        'django': {
            'handlers': ['console', ],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':LOGGING_LEVEL,
        },
        'celery.task': {
            'handlers': ['console', ],
            'propagate': True,
            'level': LOGGING_LEVEL,
        }
    }
}

# middle ware settings
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'middlewares.process_request_middleware.ProcessRequestMiddleware',
    # 'middlewares.process_session_middleware.ProcessSessionMiddleware',
]

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

# sentry_sdk.init(
#     dsn="https://42a117f659884781a1b7498e22386011@sentry.diynova.com/70",
#     integrations=[DjangoIntegration()]
# )
