from django.db import models
from .utils import ct


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


class GenericQuerySet(models.query.QuerySet):
    def create(self, **kwargs):
        return super(GenericQuerySet, self).create(
            **resolve_generic_relations(self.model, kwargs)
        )

    def _filter_or_exclude(self, negate, *args, **kwargs):
        return super(GenericQuerySet, self)._filter_or_exclude(
            negate, *args, **resolve_generic_relations(self.model, kwargs)
        )

    def get_for_object(self, content_object):
        gr_fields = getattr(self.model, '_gr_fields', {})
        if len(gr_fields) != 1:
            print(gr_fields)
            raise TypeError('This works only for models where there is the only generic relation field')
        return self.filter(**{list(gr_fields.keys())[0]: content_object})

    def get_for_model(self, model):
        return self.filter(**{self.gr_field: ct(model)})


class GenericRelationManager(models.Manager):
    # def __init__(self, *args, **kwargs):
    #     self.ct_field = kwargs.pop('ct_field', 'content_type')
    #     self.fk_field = kwargs.pop('fk_field', 'object_pk')
    #     self.gr_field = kwargs.pop('gr_field', 'content_object')
    #
    #     model = kwargs.pop('model', None)
    #
    #     if not model:
    #         self.model = model
    #     super(GenericRelationManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        #print('create queryset for', self.model)
        #print(self.model, 'id', id(self.model))
        #print('has attr', hasattr(self.model, '_gr_fields'))
        return GenericQuerySet(self.model)

    def get_for_object(self, content_object):
        return self.get_queryset().filter(**{
            self.ct_field: ct(content_object),
            self.fk_field: content_object.pk
        })

    def get_for_model(self, model):
        return self.get_queryset().filter(**{self.ct_field: ct(model)})
