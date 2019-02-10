from django.apps import apps
from django.core.cache import cache


def cache_key(model_class):
    app_label = model_class._meta.app_label
    try:
        name = model_class.__name__
    except AttributeError:
        name = model_class.__class__.__name__
    return 'ct-for-{app_label}:{name}'.format(app_label=app_label,
                                              name=name)


def resolve(model_class):
    return apps.get_model('contenttypes.ContentType')\
        .objects\
        .get_for_model(model_class)


def ct(model_class):
    """
    Shortcut for get_for_model method of ContentType manager
    """
    return cache.get_or_set(key=cache_key(model_class),
                            default=lambda: resolve(model_class))
