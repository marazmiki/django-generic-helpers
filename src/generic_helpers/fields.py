from copy import deepcopy

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from . import checks
from .managers import GenericQuerySet

CONTENT_TYPE_RELATED_NAME = 'ct_set_for_%(class)s'


@deconstructible
class AllowedContentTypes(object):
    def __init__(self, field):
        self.field = field

    def __eq__(self, other):
        return self.field.allowed_content_types() == \
               other.allowed_content_types()

    def __call__(self):
        return self.field.allowed_content_types()


class GenericRelationField(models.ForeignKey):
    foreign_key_type = models.IntegerField(_('object ID'))

    def __init__(self, **kwargs):
        self.gr_opts = {
            'replace_manager': kwargs.pop('replace_manager', False),
            'ct_field': kwargs.pop('ct_field', 'content_type'),
            'fk_field': kwargs.pop('fk_field', 'object_id'),
            'fk_field_type': kwargs.pop('fk_field_type',
                                        self.foreign_key_type),
            'allowed_content_types': kwargs.pop('allowed_content_types', None),
            'denied_content_types': kwargs.pop('denied_content_types', None),
            'manager_attr_name': kwargs.pop('manager_attr_name', 'gr'),
            'limit_choices_to': {},
            'blank': kwargs.pop('blank', False),
        }

        kwargs.update(**{
            'to': ContentType,
            'on_delete': models.CASCADE,
        })

        super().__init__(**kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(checks.check_limit_choices(self))
        errors.extend(checks.check_field_type(self))
        return errors

    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        """
        Register the field with the model class it belongs to.

        If private_only is True, create a separate instance of this field
        for every subclass of cls, even if cls is not an abstract model.
        """
        ct_field = self.gr_opts['ct_field']
        fk_field = self.gr_opts['fk_field']

        self.model_class = cls

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

        self.content_type = self.generate_contenttype_field()
        self.content_type.contribute_to_class(
            cls=cls,
            name=ct_field,
            private_only=private_only,
            **kwargs
        )
        self.foreign_key = self.generate_foreignkey_field()
        self.foreign_key.contribute_to_class(
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

        generic_relation_manager.contribute_to_class(
            self.model_class,
            self.gr_opts['manager_attr_name']
        )

        if self.gr_opts['replace_manager']:
            generic_relation_manager.contribute_to_class(
                self.model_class, 'objects'
            )
        else:
            self.model_class._default_manager.contribute_to_class(
                self.model_class, 'objects'
            )

        original_save = cls.save

        def patch_save(model_self, *args, **kwargs):
            if not self.gr_opts['blank']:
                content_type = getattr(model_self, self.content_type.name)
                self.content_type.validate(content_type.pk,  model_self)
                foreign_key = getattr(model_self, self.foreign_key.name)
                self.foreign_key.validate(foreign_key,  model_self)
            return original_save(model_self, *args, **kwargs)

        if not getattr(cls.save, 'gr_patched', False):
            docstring = cls.save.__doc__
            cls.save = patch_save
            cls.save.__doc__ = docstring
            cls.save.gr_patched = True

    def generate_foreignkey_field(self):
        field_type = deepcopy(self.gr_opts['fk_field_type'])

        if self.gr_opts['blank']:
            field_type.null = True
            field_type.blank = True
        return field_type

    def generate_contenttype_field(self):
        return models.ForeignKey(
            to=ContentType,
            on_delete=models.CASCADE,
            related_name=CONTENT_TYPE_RELATED_NAME,
            limit_choices_to=AllowedContentTypes(self),
            null=self.gr_opts['blank'],
            blank=self.gr_opts['blank'],
        )

    def allowed_content_types(self):
        # TODO: learn how to handle these types of model declaration:
        #
        # * ModelInstance (a class)
        # * 'AModelInTheSameApp' (a string without app_name)
        # * 'explicit_app.ModelClass'
        # * 'same_app.*' -- wildcard

        content_types = []
        op = self.gr_opts['allowed_content_types'] and 'filter' or 'exclude'
        gr = (self.gr_opts['allowed_content_types'] or
              self.gr_opts['denied_content_types'])

        if not gr:
            return {}

        for opt in gr:
            if isinstance(opt, (str, )):
                if '.' not in opt:
                    opt = '.'.join([self.model_class._meta.app_label, opt])
                if opt.count('.') != 1:
                    raise TypeError(
                        'Content type should be in the ``app_label.'
                        'ModelName`` format'
                    )
                app, mdl = opt.split('.')
                content_types.append(
                    ContentType.objects.get(app_label=app,
                                            model__iexact=mdl
                                            )
                )
            # An instance of model case: get_for_model() returns a set!
            elif isinstance(opt, models.Model):
                content_types.append(
                    ContentType.objects.get_for_model(opt).get()
                )
            # A class of model case: get_for_model() returns an instance!
            elif issubclass(opt, models.Model):
                content_types.append(
                    ContentType.objects.get_for_model(opt)
                )

        # Actually, this method has some issues with performance and,
        # probably, senseless at all. And it should be refactored.
        return {
            'pk__in': [
                f.id for f in getattr(ContentType.objects, op)(
                    pk__in=[c.id for c in content_types]
                )]
        } if content_types else {}


class UUIDContentField(GenericRelationField):
    """
    A generic relation field where foreign key represented as UUIDField
    """
    foreign_key_type = models.UUIDField(
        verbose_name=_('object ID'),
        help_text=_('Should be in a UUID format'),
    )


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
