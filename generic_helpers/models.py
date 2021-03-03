from __future__ import absolute_import, unicode_literals

from django.db import models

from generic_helpers.managers import GenericRelationManager
from generic_helpers.settings import USE_TEXT_OBJECT_PK

from .fields import GenericRelationField

DOCSTRING = """
{class_name}

This class is an abstract model. By inheriting from it, you
get a child model with two regular fields:

  * {ct_field}
  * {fk_field}

and one meta filed: {gr_field}

Thus your model gets a new generic relation key

"""


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
    Creates a abstract model with a generic relation key.

    The factory function produces abstract base model classes
    with **the only** generic relation foreign key.

    Probably, it's not the most flexible approach, but it's just
    work in many of products, so it should be left here.

    :param ct_field:
        Name of ForeignKey field to the ``contenttypes.ContentType``
        model. Default value is ``content_type``.
    :type ct_field: str
    :param fk_field:
        Name of ``object_id`` field. Could be different types.
        Default value is ``object_pk``
    :type fk_field: str
    :param gr_field:
        Name of ``generic foreign key`` virtual field that adds
        some useful managers. Default is ``content_object``
    :type gr_field: str
    :param manager_attr:
        Name of manager with the generic relations feature. Default
        value is ``objects``, so by default it also changes the default
        manager to generic one
    :type manager_attr: str
    :param class_name:
        Name of the dynamically created abstract model class with a
        required ``content_type`` and ``object_id`` fields. If empty or
        omitted, the name will be generated automatically.
        Default value is ``None``
    :type class_name: str|NoneType
    :param class_name_blank:
        Name of the dynamically created abstract model class with an
        optional (mean blank and nullable) content_type and object_id
        fields. If empty or omitted, the name will be generated
        automatically. Default value is ``None``
    :type class_name_blank: str|NoneType
    :param blank:
        Whether a generic foreign key could be an optional field (i.e.
        nullable and blank=True). Default value is ``False``
    :type blank: bool
    :param fk_field_type:
    :type fk_field_type: models.Field|NoneType

    :return:
    """

    fk_field_type = fk_field_type or models.CharField(max_length=255)

    class Meta(object):
        abstract = True
        index_together = [
            (ct_field, fk_field)
        ]

    if blank:
        class_name = class_name_blank or 'Blank{0}'.format(class_name)

    docstring = DOCSTRING.format(ct_field=ct_field,
                                 fk_field=fk_field,
                                 gr_field=gr_field,
                                 class_name=class_name)
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
