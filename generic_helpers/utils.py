# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib.contenttypes.models import ContentType


def ct(mdl_cls):
    """
    Shortcut for get_for_model method of ContentType manager
    """
    return ContentType.objects.get_for_model(mdl_cls)
