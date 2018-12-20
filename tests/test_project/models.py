import uuid

from django.db import models

from generic_helpers.decorators import generic_relation
from generic_helpers.fields import GenericRelationField
from generic_helpers.models import (BlankGenericRelationModel,
                                    GenericRelationModel,
                                    generic_relation_factory)


class JustModel(models.Model):
    name = models.CharField(max_length=255)


class JustAnotherModel(models.Model):
    name = models.CharField(max_length=255)


class JustUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)


class GRInheritanceExample(GenericRelationModel):
    """
    Example 1: got a required generic relation field just inherited
    from a base model without any customization
    """


class GRBlankInheritanceExample(BlankGenericRelationModel):
    """
    Example 2: got an optional generic relation field just inherited
    from a base model without any customization
    """


class GRFactoryExample(generic_relation_factory(
    gr_field='customized_content_object',
)):
    """
    Example 3: create a generic relation base model on the fly with a factory.
    """


@generic_relation
class DecoratedExample(models.Model):
    """
    Example 4: got a generic relation by means of @generic_relation decorator
    """


@generic_relation(
    blank=True,
    gr_field='customized_content_object'
)
class DecoratedCustomizeExample(models.Model):
    """
    Example 5: got a customized generic relation with @generic_relation
    decorator with some params.
    """


@generic_relation(gr_field='gr2', ct_field='ct2', fk_field='fk2')
@generic_relation(gr_field='gr1', ct_field='ct1', fk_field='fk1')
class DecoratedTwiceExample(models.Model):
    """
    Example 6: we can multiple decorate a model class to get some
    generic relation fields
    """


class ExampleField(models.Model):
    """
    Example 7: arbitrary generic relation
    """
    content_object = GenericRelationField()


class ExampleReplaceManager(models.Model):
    """
    Example 8: replace a default manager on a model class
    """
    content_object = GenericRelationField(replace_manager=True)


class ExamplePrimaryKeyFieldType(models.Model):
    """
    Example 9: replace a default manager on a model class
    """
    content_object = GenericRelationField(
        fk_field_type=models.UUIDField()
    )


class ExampleManagerName(models.Model):
    """
    Example 10: generic relation field adds a generic relation manager
    attribute with the given name.
    """
    content_object = GenericRelationField(manager_attr_name='gr_mgr')


class ContentTypeWhiteList(models.Model):
    """
    Example 11: limited content type choice. The white list strategy
    """
    content_object = GenericRelationField(
        allow_content_types=['JustModel',
                             'contenttypes.ContentType']
    )


class ContentTypeBlackList(models.Model):
    """
    Example 12: limited content type choice. The black list strategy
    """
    content_object = GenericRelationField(
        deny_content_types=[JustModel]
    )
