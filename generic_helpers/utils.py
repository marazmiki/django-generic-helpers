from django.apps import apps
from django.core.cache import cache


def cache_key(model_class):
    return (
        'ct-for-{model_class.app_label}:{model_class.__class__.__name__}'
    ).format(model_class=model_class)


def resolve(model_class):
    return apps.get_model('contenttypes.ContentType')\
        .objects\
        .get_for_model(model_class)


def ct(model_class):
    """
    Shortcut for get_for_model method of ContentType manager
    """
    return resolve(model_class)
    return cache.get_or_set(key=cache_key(model_class),
                            default=lambda: resolve(model_class)
                            )
