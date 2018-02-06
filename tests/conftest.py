import pytest


STORY_NUMBER = 5
PICTURE_NUMBER = 4
COMMENT_NUMBER = 3
VOTING_CT_NAME = 'buzz'


def pytest_configure():
    pass


@pytest.fixture
def BuzzGRM():
    from generic_helpers.models import generic_relation_factory
    return generic_relation_factory(gr_field=VOTING_CT_NAME)


def Story():
    from django.db import models

    class Story(models.Model):
        text = models.TextField()

        class Meta(object):
            app_label = 'generic_helpers'

    return Story


class Picture(models.Model):
    url = models.URLField(max_length=255)

    class Meta(object):
        app_label = 'generic_helpers'


class Comment(GRM):
    body = models.TextField(max_length=255)

    class Meta(object):
        app_label = 'generic_helpers'


class Voting(BuzzGRM):
    score = models.IntegerField(default=1)

    class Meta(object):
        app_label = 'generic_helpers'
