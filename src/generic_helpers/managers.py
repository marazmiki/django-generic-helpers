import django
from django.db import models

from .utils import ct, resolve_generic_relations


class GenericQuerySet(models.query.QuerySet):
    """
    A QuerySet with an improved generic relations support
    """

    def create(self, **kwargs):
        """
        Create a new object with the given kwargs, saving it to the database
        and returning the created object.

        If there are "generic foreign keys" inside the kwargs, it also will
        be handled correctly.
        """
        return super().create(**resolve_generic_relations(self.model, kwargs))

    if django.__version__ >= '3.2':
        def _filter_or_exclude(self, negate, args, kwargs):
            new_kwargs = resolve_generic_relations(self.model, kwargs)
            return super()._filter_or_exclude(negate, args, new_kwargs)
    else:
        def _filter_or_exclude(self, negate, *args, **kwargs):
            new_kwargs = resolve_generic_relations(self.model, kwargs)
            return super()._filter_or_exclude(negate, *args, **new_kwargs)

    def get_for_object(self, content_object):
        gr_fields = getattr(self.model, '_gr_fields', {})
        if len(gr_fields) != 1:
            raise TypeError('It works only for models where there is the '
                            'only generic relation field')
        if django.__version__ >= '3.2':
            fields = list(gr_fields.values())[0]
            return self.filter(**{
                fields['ct_field']: ct(content_object),
                fields['fk_field']: content_object.pk,
            })
        else:
            return self.filter(**{list(gr_fields.keys())[0]: content_object})

    def get_for_model(self, model):
        return self.filter(**{self.gr_field: ct(model)})


class GenericRelationManager(models.Manager):
    def get_queryset(self):
        return GenericQuerySet(self.model)

    def get_for_object(self, content_object):
        return self.get_queryset().filter(**{
            self.ct_field: ct(content_object),
            self.fk_field: content_object.pk
        })

    def get_for_model(self, model):
        return self.get_queryset().filter(**{self.ct_field: ct(model)})
