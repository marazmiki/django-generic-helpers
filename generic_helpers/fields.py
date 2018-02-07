from copy import deepcopy
from django.db import models
from django.core import checks
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from .managers import GenericQuerySet


CONTENT_TYPE_RELATED_NAME = 'ct_set_for_%(class)s'


class GenericRelationField(models.ForeignKey):
    foreign_key_type = models.IntegerField(_('object ID'))

    def __init__(self, **kwargs):
        self.gr_opts = {
            'replace_manager': kwargs.pop('replace_manager', False),
            'ct_field': kwargs.pop('ct_field', 'content_type'),
            'fk_field': kwargs.pop('fk_field', 'object_id'),
            'fk_field_type': kwargs.pop('fk_field_type', self.foreign_key_type),
            'allow_content_types': kwargs.pop('allow_content_types', None),
            'deny_content_types': kwargs.pop('deny_content_types', None),
            'manager_attr_name': kwargs.pop('manager_attr_name', 'gr'),
            'limit_choices_to': {},
            'blank': kwargs.pop('blank', False),
        }

        kwargs.update(**{
            'to': 'contenttypes.ContentType',
            'on_delete': models.CASCADE,
        })

        super(GenericRelationField, self).__init__(**kwargs)

    def check(self, **kwargs):
        errors = super(GenericRelationField, self).check(**kwargs)
        errors.extend(self._check_limit_choices())
        errors.extend(self._check_field_type())
        return errors

    def _check_field_type(self):
        if not isinstance(self.gr_opts['fk_field_type'], models.Field):
            return [
                checks.Error(
                    msg=(
                        'if you need to change a foreign key field '
                        'type (e.g. UUID), you must provide a field '
                        'instanced object.'
                    ),
                    hint=(
                        'You should provide either "allow_content_types" '
                        'parameter, or "deny_content_types" one. Or, if '
                        'you don\'t need any limitation, just miss '
                        'this parameter.'
                    ),
                    obj=self,
                    id='generic_helpers.E002',
                )
            ]
        else:
            return []

    def _check_limit_choices(self):
        if all((
            self.gr_opts['allow_content_types'],
            self.gr_opts['deny_content_types']
        )):
            return [
                checks.Error(
                    msg=(
                        'Wrong generic relation limits specified: you\'ve '
                        'provided both "allow" and "deny" list.'
                    ),
                    hint=(
                        'You should provide either "allow_content_types" '
                        'parameter, or "deny_content_types" one. Or, if '
                        'you don\'t need any limitation, just miss '
                        'this parameter.'
                    ),
                    obj=self,
                    id='generic_helpers.E001',
                )
            ]
        else:
            return []

    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        """
        Register the field with the model class it belongs to.

        If private_only is True, create a separate instance of this field
        for every subclass of cls, even if cls is not an abstract model.
        """
        ct_field = self.gr_opts['ct_field']
        fk_field = self.gr_opts['fk_field']

        # Customize the content-type field name
        if not ct_field:
            ct_field = '{0}_content_type'.format(name)
            if name == 'content_object':
                ct_field = 'content_type'

        # Customize the object id field name
        if not fk_field:
            fk_field = '{0}_object_id'.format(name)
            if name == 'content_object':
                fk_field = 'object_id'

        content_type = self.generate_contenttype_field()
        content_type.contribute_to_class(
            cls=cls,
            name=ct_field,
            private_only=private_only,
            **kwargs
        )

        foreign_key = self.generate_foreignkey_field()
        foreign_key.contribute_to_class(
            cls=cls,
            name=fk_field,
            private_only=private_only
        )

        if not hasattr(cls, '_gr_fields'):
            setattr(cls, '_gr_fields', {})

        # And what if it's already here?
        cls._gr_fields[name] = {
            'ct_field': self.gr_opts['ct_field'],
            'fk_field': self.gr_opts['fk_field']
        }

        generic_relation_manager = GenericQuerySet(cls).as_manager()

        GenericForeignKey(
            ct_field=self.gr_opts['ct_field'],
            fk_field=self.gr_opts['fk_field'],
        ).contribute_to_class(cls, name)

        setattr(cls, self.gr_opts['manager_attr_name'],
                deepcopy(generic_relation_manager))

        if self.gr_opts['replace_manager']:
            setattr(cls, 'objects', generic_relation_manager)

    def get_limit_choices_to(self):
        return {'id__in': [ct.id for ct in self.allowed_content_types]}

    def generate_foreignkey_field(self):
        field_type = deepcopy(self.gr_opts['fk_field_type'])

        if self.gr_opts['blank']:
            field_type.null = True
            field_type.blank = True
        return field_type

    def generate_contenttype_field(self):
        return models.ForeignKey(
            to='contenttypes.ContentType',
            on_delete=models.CASCADE,
            related_name=CONTENT_TYPE_RELATED_NAME,
            limit_choices_to=self.get_limit_choices_to,
            null=self.gr_opts['blank'],
            blank=self.gr_opts['blank'],
        )

    @cached_property
    def all_content_types(self):
        return ContentType.objects.all()

    @cached_property
    def allowed_content_types(self):
        if not any((
            self.gr_opts['allow_content_types'],
            self.gr_opts['deny_content_types'],
        )):
            return self.all_content_types

        if self.gr_opts['allow_content_types']:
            print('*** allow', self.model)
            pass

        if self.gr_opts['deny_content_types']:
            print('**** deny', self.model)
            pass

        return self.all_content_types

#
# ModelInstance
# 'ModelTheSameApp'
# 'same_app.ModelTheSameApp'
# 'another_app.AnotherModel'
# 'same_app.*'



class UUIDContentField(GenericRelationField):
    """
    A generic relation field where foreign key represented as UUIDField
    """
    foreign_key_type = models.UUIDField(_('object ID'))


class TextContentField(GenericRelationField):
    """
    A generic relation field where foreign key represented as TextField
    """
    foreign_key_type = models.TextField(_('object ID'))


class CharContentField(GenericRelationField):
    """
    A generic relation field where foreign key represented as CharField
    """
    foreign_key_type = models.CharField(_('object ID'), max_length=255)
