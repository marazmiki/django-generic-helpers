# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from generic_helpers.managers import GenericRelationManager
from generic_helpers.settings import USE_TEXT_OBJECT_PK


try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

# Default value for `related_name` argument
CONTENT_TYPE_RELATED_NAME = 'ct_set_for_%(class)s'


def generic_relation_factory(ct_field='content_type', fk_field='object_pk',
                             gr_field='content_object', manager_attr='objects',
                             ct_related_name=None,
                             class_name='GenericRelationModel',
                             class_name_blank=None, blank=False,
                             fk_field_type=None):
    """
    """
    ct = models.ForeignKey(ContentType,
                           related_name=(ct_related_name or
                                         CONTENT_TYPE_RELATED_NAME),
                           verbose_name=_('content type'),
                           blank=blank, null=blank)

    if fk_field_type is None:
        fk_field_type = models.CharField(_('object ID'), max_length=255,
                                         default='', blank=blank, null=blank)
    fk = fk_field_type

    gr = GenericForeignKey(ct_field=ct_field, fk_field=fk_field)

    class Meta(object):
        abstract = True
        index_together = [(ct_field, fk_field)]

    # If
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

    manager = GenericRelationManager(ct_field=ct_field, fk_field=fk_field,
                                     gr_field=gr_field)

    return type(class_name, (models.Model, ), {ct_field: ct,
                                               fk_field: fk,
                                               gr_field: gr,
                                               manager_attr: manager,
                                               'Meta': Meta,
                                               '__module__': __name__,
                                               '__doc__': docstring
                                               })

if USE_TEXT_OBJECT_PK:
    GenericRelationModel = generic_relation_factory()
    BlankGenericRelationModel = generic_relation_factory(blank=True)
else:
    fk_field_type = models.IntegerField(_('Object ID'), default=0)
    GenericRelationModel = generic_relation_factory(
        fk_field_type=fk_field_type
    )
    BlankGenericRelationModel = generic_relation_factory(
        fk_field_type=fk_field_type,
        blank=True
    )
