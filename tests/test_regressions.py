import pytest

from generic_helpers.fields import GenericRelationField
from test_project.models import JustModel, VolodyRegression


def test_model_name_startswith__aka_busy_regression():
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


def test_model_save_patch__aka_volody2006_regression():
    with pytest.raises(ZeroDivisionError):
        volody = VolodyRegression()
        volody.content_object = JustModel.objects.create()
        volody.save()
