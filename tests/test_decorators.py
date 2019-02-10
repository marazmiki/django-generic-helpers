from test_project.models import (DecoratedCustomizeExample, DecoratedExample,
                                 DecoratedTwiceExample)


def ex(model_class, content_object, field_name='content_object'):
    instance = model_class.objects.create(**{field_name: content_object})
    instance = model_class.objects.get(pk=instance.pk)
    return instance


def test_decorator_default_values(just_model):
    example = ex(DecoratedExample,
                 content_object=just_model)
    assert example.content_object == just_model


def test_decorator_with_customization(just_model):
    example = ex(DecoratedCustomizeExample,
                 content_object=just_model,
                 field_name='customized_content_object')
    assert example.customized_content_object == just_model


def test_decorated_twice(just_model, just_another_model):
    model = DecoratedTwiceExample()
    model.gr1 = just_model
    model.gr2 = just_another_model
    model.save()

    model = DecoratedTwiceExample.objects.get(pk=model.id)

    assert model.gr1 == just_model
    assert model.gr2 == just_another_model
