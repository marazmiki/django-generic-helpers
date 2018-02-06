An old way
==========

.. code:: python

    from django.db import models
    from generic_helpers.models import GenericRelationModel

    class Vote(GenericRelationModel):
        pass


And for optional fields:


.. code:: python


    from generic_helpers.models import BlankGenericRelationModel

    class Vote(BlankGenericRelationModel):
        pass

    from generic_helpers.decorators import generic_relation

    @generic_relation('content_object', ct_field='content_type', pk_field='o_id')
    @generic_relation('content_object', ct_field='content_type', pk_field='o_id')
    class Vote(models.Model):
        pass





A new way
=========

    from django.db import models
    from generic_helpers.fields import GenericRelationField

    class Vote(models.Model)
        content_object = GenericRelationField(
            replace_manager=False,
            ct_field='content_type',
            pk_field='object_pk',
            pk_field_type=models.IntegerField, # or models.UUIDField,
            allow_content_types=[],
            deny_content_types=[],
            manager_name='gr',
        )


Managers and querysets
======================

    post = Post.objects.get(pk=1)

    Vote.objects.get_for_object(content_object=post)

Filtering allowed here:

    Vote.objects.get_for_object(content_object=post).filter(content_object__user=None) # Is it possible?
