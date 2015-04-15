# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django import get_version
from generic_helpers.utils import ct


class GenericQuerySet(models.query.QuerySet):
    def __init__(self, *args, **kwargs):
        self.ct_field = kwargs.pop('ct_field', 'content_type')
        self.fk_field = kwargs.pop('fk_field', 'object_pk')
        self.gr_field = kwargs.pop('gr_field', 'content_object')
        super(GenericQuerySet, self).__init__(*args, **kwargs)

    def _filter_or_exclude(self, negate, *args, **kwargs):
        if self.gr_field in kwargs:
            instance = kwargs.pop(self.gr_field)
            kwargs.update(**{self.ct_field: ct(instance),
                             self.fk_field: instance.pk
                             })
        return super(GenericQuerySet, self)._filter_or_exclude(negate, *args,
                                                               **kwargs)

    def get_for_object(self, content_object):
        return self.filter(**{self.gr_field: content_object})

    def get_for_model(self, model):
        return self.filter(**{self.gr_field: ct(model)})


class GenericRelationManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.ct_field = kwargs.pop('ct_field', 'content_type')
        self.fk_field = kwargs.pop('fk_field', 'object_pk')
        self.gr_field = kwargs.pop('gr_field', 'content_object')
        super(GenericRelationManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return GenericQuerySet(self.model, ct_field=self.ct_field,
                               fk_field=self.fk_field, gr_field=self.gr_field)

    if get_version() < '1.7':
        def get_query_set(self):
            return self.get_queryset()

    def get_for_object(self, content_object):
        return self.get_queryset().filter(**{
            self.ct_field: ct(content_object),
            self.fk_field: content_object.pk
        })

    def get_for_model(self, model):
        return self.get_queryset().filter(**{self.ct_field: ct(model)})
