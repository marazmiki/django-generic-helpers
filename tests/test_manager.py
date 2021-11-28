from test_project.models import ExampleField, JustAnotherModel, JustModel


def test_queryset_filter():
    object_a = JustModel.objects.create()
    object_b = JustAnotherModel.objects.create()

    found = [
        ExampleField.objects.create(content_object=object_a)
        for _ in range(3)
    ]
    not_found = [
        ExampleField.objects.create(content_object=object_b)
    ]
    queryset = ExampleField.objects.filter(content_object=object_a)

    assert all((
        instance in found
        for instance in queryset
    ))
    assert all((
        instance not in not_found
        for instance in queryset
    ))
