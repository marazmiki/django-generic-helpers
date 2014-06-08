# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from generic_helpers.models import (GenericRelationModel as GRM,
                                    generic_relation_factory)


STORY_NUMBER = 5
PICTURE_NUMBER = 4
COMMENT_NUMBER = 3
VOTING_CT_NAME = 'buzz'


BuzzGRM = generic_relation_factory(gr_field=VOTING_CT_NAME)


class Story(models.Model):
    text = models.TextField()

    class Meta(object):
        app_label = 'generic_helpers'


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
