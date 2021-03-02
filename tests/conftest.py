import pytest
from test_project import models as m  # noqa


@pytest.fixture(autouse=True)
def autouse_db(db):
    "Make Django automatically use a database connection everywhere"


@pytest.fixture
def just_model():
    return m.JustModel.objects.create(name='A model')


@pytest.fixture
def just_another_model():
    return m.JustAnotherModel.objects.create(name='Yet another model')


@pytest.fixture
def just_uuid_model():
    return m.JustUUIDModel.objects.create(name='A model with UUID primary key')
