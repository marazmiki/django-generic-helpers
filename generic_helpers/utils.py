from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType


def resolve(model_class):
    return ContentType.objects.get_for_model(model_class)


def ct(model_class):
    """
    Shortcut for get_for_model method of ContentType manager
    """
    return cache.get_or_set(
        key='ct-for-{m.app_label}:{m.__class__.__name__}'.format(m=model_class),
        default=lambda: resolve(model_class)
    )


