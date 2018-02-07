import pytest
from django.apps import apps
from django.core.exceptions import ValidationError
from test_project import models as m


def ex(model_class, content_object, field_name='content_object'):
    instance = model_class.objects.create(**{field_name: content_object})
    instance = model_class.objects.get(pk=instance.pk)
    return instance


def test_1(just_model):
    example = ex(m.GRInheritanceExample, just_model)
    assert example.content_object == just_model


def test_2():
    example = ex(m.GRBlankInheritanceExample, None)
    assert example.content_object is None


def test_3(just_model):
    example = ex(m.GRFactoryExample,
                 content_object=just_model,
                 field_name='customized_content_object')

    assert example.customized_content_object == just_model


@pytest.mark.skip
def test_4(just_model):
    example = ex(m.DecoratedExample,
                 content_object=just_model)
    assert example.content_object == just_model


@pytest.mark.skip
def test_5(just_model):
    example = ex(m.DecoratedCustomizeExample,
                 content_object=just_model,
                 field_name='customized_content_object')
    assert example.customized_content_object == just_model


@pytest.mark.skip
def test_6(just_model, just_another_model):
    model = m.DecoratedTwiceExample()
    model.content_object = just_model
    model.another_generic_relation = just_another_model
    model.save()

    model = m.DecoratedTwiceExample.objects.get(pk=model.id)

    assert model.content_object == just_model
    assert model.another_generic_relation == just_another_model


def test_7(just_model):
    example = ex(m.ExampleField, content_object=just_model)
    assert example.content_object == just_model


def test_8(just_model):
    model = ex(m.ExampleReplaceManager, content_object=just_model)
    assert model in m.ExampleReplaceManager.objects.get_for_object(just_model)


def test_9a(just_uuid_model):
    model = ex(m.ExamplePrimaryKeyFieldType, content_object=just_uuid_model)
    assert model.content_object == just_uuid_model


def test_9b(just_model):
    with pytest.raises(ValidationError):
        ex(m.ExamplePrimaryKeyFieldType, content_object=just_model)


def test_10(just_model):
    model = ex(m.ExampleManagerName, just_model)
    assert model in m.ExampleManagerName.gr_mgr.get_for_object(just_model)


@pytest.mark.parametrize(
    argnames='model_name, error_expected',
    argvalues=[
        ('test_project.JustModel', False),
        ('test_project.JustAnotherModel', True),
    ],
    ids=[
        'model of allowed type must be added',
        'model of disallowed class must cause an exception',
    ])
def test_11a(model_name, error_expected):


    model_class = apps.get_model(model_name)

    content_object = model_class(name=model_name)
    content_object.save()

    if error_expected:
        with pytest.raises(ValidationError):
            ex(m.ContentTypeWhiteList, content_object)

    else:
        model = ex(m.ContentTypeWhiteList, content_object)
        assert model.content_object == content_object

