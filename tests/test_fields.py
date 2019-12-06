import pytest
from django import VERSION
from django.apps import apps
from django.core.exceptions import ValidationError

from generic_helpers.fields import GenericRelationField
from test_project.models import (ContentTypeBlackList, ContentTypeWhiteList,
                                 ExampleField, ExampleManagerName,
                                 ExamplePrimaryKeyFieldType,
                                 ExampleReplaceManager, JustModel)


def ex(model_class, content_object, field_name='content_object'):
    instance = model_class.objects.create(**{field_name: content_object})
    instance = model_class.objects.get(pk=instance.pk)
    return instance


def test_7(just_model):
    example = ex(ExampleField, content_object=just_model)
    assert example.content_object == just_model


def test_8(just_model):
    model = ex(ExampleReplaceManager, content_object=just_model)
    assert model in ExampleReplaceManager.objects.get_for_object(just_model)


def test_9a(just_uuid_model):
    model = ex(ExamplePrimaryKeyFieldType, content_object=just_uuid_model)
    assert model.content_object == just_uuid_model


@pytest.mark.skipif(
    condition=VERSION >= (2, 2),
    reason='Fails on Django 2.2x due new version of SQLite?'
)
def test_9b(just_model):
    with pytest.raises(ValidationError):
        ex(ExamplePrimaryKeyFieldType, content_object=just_model)


def test_10(just_model):
    model = ex(ExampleManagerName, just_model)
    assert model in ExampleManagerName.gr_mgr.get_for_object(just_model)


@pytest.mark.parametrize(
    argnames='model_name, error_expected',
    argvalues=[
        ('test_project.JustModel', False),
        ('test_project.JustAnotherModel', True),
    ],
    ids=[
        'a model of allowed type should be added',
        'a model of disallowed class should cause an exception',
    ])
def test_11a(model_name, error_expected):
    model_class = apps.get_model(model_name)

    content_object = model_class(name=model_name)
    content_object.save()

    if error_expected:
        with pytest.raises(ValidationError):
            ex(ContentTypeWhiteList, content_object)
    else:
        model = ex(ContentTypeWhiteList, content_object)
        assert model.content_object == content_object


@pytest.mark.parametrize(
    argnames='model_name, error_expected',
    argvalues=[
        ('test_project.JustModel', True),
        ('test_project.JustAnotherModel', False),
    ],
    ids=[
        'a model of disallowed class should cause an exception',
        'a model of non-disallowed class should be added',
    ])
def test_12(model_name, error_expected):
    model_class = apps.get_model(model_name)

    content_object = model_class(name=model_name)
    content_object.save()

    if error_expected:
        with pytest.raises(ValidationError):
            ex(ContentTypeBlackList, content_object)
    else:
        model = ex(ContentTypeBlackList, content_object)
        assert model.content_object == content_object


def test_14():
    """
    It's a regression test for an issue discovered by @busy when
    allowed_content_type() failed when there are some models
    started with the same substring (e.g. Example and ExampleTwo)
    """
    field = GenericRelationField(allowed_content_types=['Example'])
    field.model_class = JustModel
    assert isinstance(
        field.allowed_content_types(),
        dict
    )
