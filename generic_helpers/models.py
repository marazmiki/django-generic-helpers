# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from generic_helpers.managers import GenericRelationManager
from generic_helpers.settings import USE_TEXT_OBJECT_PK
from .fields import GenericRelationField


def generic_relation_factory(
        ct_field='content_type',
        fk_field='object_pk',
        gr_field='content_object',
        manager_attr='objects',
        class_name='GenericRelationModel',
        class_name_blank=None,
        blank=False,
        fk_field_type=None
):
    """

    :param ct_field:
    :type ct_field:

    :param fk_field:
    :type fk_field:

    :param gr_field:
    :type gr_field:

    :param manager_attr:
    :type manager_attr:

    :param ct_related_name:
    :type ct_related_name:

    :param class_name:
    :type class_name:

    :param class_name_blank:
    :type class_name_blank:

    :param blank:
    :type blank:

    :param fk_field_type:
    :type fk_field_type:

    :return:
    """

    fk_field_type = fk_field_type or models.CharField(max_length=255)

    class Meta(object):
        abstract = True
        index_together = [
            (ct_field, fk_field)
        ]

    if blank:
        class_name = class_name_blank or 'Blank%s' % class_name

    if not six.PY3:
        class_name = six.binary_type(class_name)

    docstring = """
    %(class_name)s

    This class is an abstract model. By inheriting from it, inherited
    model gets two regular fields:

      * %(ct_field)s
      * %(fk_field)s

    And one meta filed: %(gr_field)s

    Thus your model gets new genric relation key

    """ % {'ct_field': ct_field,
           'fk_field': fk_field,
           'gr_field': gr_field,
           'class_name': class_name}

    return type(class_name, (models.Model, ), {
        gr_field: GenericRelationField(
            replace_manager=True,
            ct_field=ct_field,
            fk_field=fk_field,
            fk_field_type=fk_field_type,
            manager_attr_name='objects',
            blank=blank,
        ),
        manager_attr: GenericRelationManager(),
        'Meta': Meta,
        '__module__': __name__,
        '__doc__': docstring
    })


if USE_TEXT_OBJECT_PK:
    GenericRelationModel = generic_relation_factory()
    BlankGenericRelationModel = generic_relation_factory(blank=True)

else:
    GenericRelationModel = generic_relation_factory(
        fk_field_type=models.IntegerField()
    )
    BlankGenericRelationModel = generic_relation_factory(
        fk_field_type=models.IntegerField(null=True),
        blank=True
    )
