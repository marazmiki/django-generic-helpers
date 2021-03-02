from django.contrib.contenttypes.models import ContentType
from test_project.models import JustModel

from generic_helpers.utils import ct


def test_ct_works_for_model_class():
    assert isinstance(ct(JustModel), ContentType)


def test_ct_works_for_model_instances():
    assert isinstance(ct(JustModel(name='Oh wow')), ContentType)
