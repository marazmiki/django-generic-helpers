# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf import settings

USE_TEXT_OBJECT_PK = getattr(settings, 'GENERIC_HELPERS_USER_TEXT_OBJECT_PK',
                             True)
