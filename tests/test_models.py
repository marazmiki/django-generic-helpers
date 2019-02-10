from test_project.models import (GRBlankInheritanceExample, GRFactoryExample,
                                 GRInheritanceExample)


def ex(model_class, content_object, field_name='content_object'):
    instance = model_class.objects.create(**{field_name: content_object})
    instance = model_class.objects.get(pk=instance.pk)
    return instance


def test_1(just_model):
    example = ex(GRInheritanceExample, just_model)
    assert example.content_object == just_model


def test_2():
    example = ex(GRBlankInheritanceExample, None)
    assert example.content_object is None


def test_3(just_model):
    example = ex(GRFactoryExample,
                 content_object=just_model,
                 field_name='customized_content_object')

    assert example.customized_content_object == just_model
