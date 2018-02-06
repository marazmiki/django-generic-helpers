from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.fields import GenericForeignKey


class GenericRelationField(models.ForeignKey):
    def __init__(self, **kwargs):
        self.gr_opts = {
            'replace_manager': kwargs.pop('replace_manager', False),
            'ct_field': kwargs.pop('ct_field', 'content_type'),
            'pk_field': kwargs.pop('pk_field', 'object_pk'),
            'pk_field_type': kwargs.pop('pk_field_type', models.IntegerField),
            'allow_content_types': kwargs.pop('allow_content_types', None),
            'deny_content_types': kwargs.pop('deny_content_types', None),
            'manager_attr_name': kwargs.pop('manager_attr_name', 'gr'),
            'limit_choices_to': {},
        }

        if not issubclass(self.gr_opts['pk_field_type'], models.Field):
            raise ImproperlyConfigured(
                'Make sure the pk_field_type is a class inherited from '
                'the models.Field base'
            )

        if all((
            self.gr_opts['allow_content_types'],
            self.gr_opts['deny_content_types']
        )):
            raise ImproperlyConfigured(
                'You should specify either allow_content_types, or '
                'deny_content_types. No both the same time'
            )

        kwargs.update(**{
            'to': 'contenttypes.ContentType',
            'on_delete': models.CASCADE,
        })

        super(GenericRelationField, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        models.ForeignKey(
            to='contenttypes.ContentType',
            on_delete=models.CASCADE,
            limit_choices_to=self.get_limit_choices_to(),
        ).contribute_to_class(cls, self.gr_opts['pk_field'],
                              private_only, **kwargs)
        self.gr_opts['pk_field_type'](
            editable=False,
            null=True
        ).contribute_to_class(cls, self.gr_opts['pk_field'], private_only)

        if not hasattr(cls, '_gr_fields'):
            setattr(cls, '_gr_fields', [])

        cls._gr_fields.append(name)

        setattr(cls, name, GenericForeignKey(
            ct_field=self.gr_opts['ct_field'],
            fk_field=self.gr_opts['pk_field'],
        ))

    def get_limit_choices_to(self):
        if self.gr_opts['allow_content_types']:
            pass
        if self.gr_opts['deny_content_types']:
            pass
