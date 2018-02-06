from django.db import models
from generic_helpers.decorators import generic_relation
from generic_helpers.fields import GenericRelationField
from generic_helpers.models import (
    GenericRelationModel,
    BlankGenericRelationModel,
    generic_relation_factory,
)


class JustModel(models.Model):
    name = models.CharField(max_length=255)


class JustAnotherModel(models.Model):
    name = models.CharField(max_length=255)


class GRExample(GenericRelationModel):
    """
    Example 1: got a required generic relation field just inherited
    from a base model without any customization
    """


class GRBlankExample(BlankGenericRelationModel):
    """
    Example 2: got an optional generic relation field just inherited
    from a base model without any customization
    """


class GRFactoryExample(generic_relation_factory(
    gr_field='customized_content_object',
)):
    """
    Example 3: create a genric relation base model on the fly with a factory.
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

@generic_relation
@generic_relation(gr_field='another_generic_relation')
class DecoratedTwiceExample(models.Model):
    """
    Example 6: we can multiple decorate a model class to get some
    generic relation fields
    """


class ExampleField(models.Model):
    """
    Example 7: arbitrary generic relation
    """
    generic_relation = GenericRelationField()


class ExampleReplaceManager(models.Model):
    generic_relation = GenericRelationField(replace_manager=False)


class ExamplePrimaryKeyFieldType(models.Model):
    generic_relation = GenericRelationField(pk_field_type=models.UUIDField)


class ExampleManagerName(models.Model):
    generic_relation = GenericRelationField(manager_name='gr_mgr')


class ContentTypeWhiteList(models.Model):
    generic_relation = GenericRelationField(
        allow_content_types=['JustModel', 'contenttypes.ContentType']
    )


class ContentTypeBlackList(models.Model):
    generic_relation = GenericRelationField(
        deny_content_types=[JustModel]
    )
