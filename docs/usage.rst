Usage
#####



An old way
==========

The old way we've added generic fields to an orbitrary model was an
inheritance from the base abstract ``GenericRelationModel`` model.

.. code:: python

    from django.db import models
    from generic_helpers.models import GenericRelationModel

    class Vote(GenericRelationModel):
        pass

or from ``BlankGenericRelationModel`` to get an optional field:


.. code:: python

    from generic_helpers.models import BlankGenericRelationModel

    class Vote(BlankGenericRelationModel):
        pass


Well, it wasn't quite usable, because a model could have the only generic
relation field with a fixed name.


.. code:: python

    from generic_helpers.decorators import generic_relation

    @generic_relation('content_object', ct_field='content_type', pk_field='o_id')
    @generic_relation('content_object', ct_field='content_type', fk_field='o_id')
    class Vote(models.Model):
        pass


A new way
=========

With a new one, we just declare a generic relation field like as usual model one.

.. code:: python

    from django.db import models
    from generic_helpers.fields import GenericRelationField

    class Vote(models.Model)
        content_object = GenericRelationField(
            replace_manager=False,                  # 1
            manager_name='gr',                      # 2
            ct_field='content_type',                # 3
            fk_field='object_pk',                   # 4
            fk_field_type=models.IntegerField(),    # 5
            allowed_content_types=[],                 # 6
            denied_content_types=[],                  # 7

            # ...and other keyword arguments that
            # the ForeignKey field accepts
        )

With this, you can create an arbitrary number of generic relation fields with
different options and customized managers.


.. code:: python

    Vote.objects.filter(content_object=my_post)

2)






Managers and querysets
======================

    post = Post.objects.get(pk=1)

    Vote.objects.get_for_object(content_object=post)

Filtering allowed here:

    Vote.objects.get_for_object(content_object=post).filter(content_object__user=None) # Is it possible?
