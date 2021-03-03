from django.conf import settings

USE_TEXT_OBJECT_PK = getattr(settings, 'GENERIC_HELPERS_USER_TEXT_OBJECT_PK',
                             True)
