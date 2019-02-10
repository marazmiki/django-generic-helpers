Synopsis
########

The django application aimed to simplify work with generic relation and brings
some syntax sugar to it.


The first purpose the library was written is ability to make queryset filtering
through generic relation fields like it was normal ones.

.. code:: python

    Comment.objects.filter(content_type=blog_post)


The ct helper
=============

One of the most useful features of the package is a small function called ``ct()``.
It just return a

