from django.apps import apps
from django.core.cache import cache

CACHE_KEY = 'ct-for-{app_label}:{class_name}'


def cache_key(model_class):
    app_label = model_class._meta.app_label
    try:
        name = model_class.__name__
    except AttributeError:
        name = model_class.__class__.__name__
    return 'ct-for-{app_label}:{name}'.format(app_label=app_label, name=name)


def resolve(model_class):
    return apps.get_model('contenttypes.ContentType')\
        .objects\
        .get_for_model(model_class)


def ct(model_class):
    """
    Shortcut for get_for_model method of ContentType manager
    """
    return cache.get_or_set(key=cache_key(model_class),
                            default=lambda: resolve(model_class)
                            )


def resolve_generic_relations(model_class, filter_kwargs):
    gr_fields = getattr(model_class, '_gr_fields', {})
    new_filters = {}
    for field in list(filter_kwargs.keys()):
        if field not in gr_fields:
            new_filters[field] = filter_kwargs[field]
        else:
            content_object = filter_kwargs[field]
            ct_field = gr_fields[field]['ct_field']
            fk_field = gr_fields[field]['fk_field']
            new_filters.update(**{
                ct_field: ct(content_object) if content_object else None,
                fk_field: content_object.pk if content_object else None
            })
    return new_filters
