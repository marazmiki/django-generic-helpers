======================
django-generic-helpers
======================

.. image:: https://badge.fury.io/py/django-generic-helpers.svg
   :target: http://badge.fury.io/py/django-generic-helpers

.. image:: https://travis-ci.org/marazmiki/django-generic-helpers.svg?branch=master
   :target: https://travis-ci.org/marazmiki/django-generic-helpers

.. image:: https://coveralls.io/repos/marazmiki/django-generic-helpers/badge.svg?branch=master
   :target: https://coveralls.io/r/marazmiki/django-generic-helpers?branch=master

.. image:: https://pypip.in/d/django-generic-helpers/badge.png
   :target: https://pypi.python.org/pypi/django-generic-helpers

.. image:: https://pypip.in/wheel/django-generic-helpers/badge.svg
   :target: https://pypi.python.org/pypi/django-generic-helpers/
   :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/django-generic-helpers.svg
   :target: https://pypi.python.org/pypi/django-generic-helpers/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/djversions/django-generic-helpers.svg
   :target: https://pypi.python.org/pypi/django-generic-helpers/
   :alt: Supported Django versions


The application provides some syntax sugar for working with Django's `generic relations <https://docs.djangoproject.com/en/2.2/ref/contrib/contenttypes/#generic-relations>`_



Installation
============

Just install the package from PyPI within ``pip``

.. code:: bash

    pip install django-generic-helpers

...or `pipenv <https://docs.pipenv.org/en/latest/>`_

.. code:: bash

    pipenv install django-generic-helpers

...or even `poetry <https://poetry.eustace.io/>`_

.. code:: bash

    poetry add django-generic-helpers

That's all. No need to add this into ``INSTALLED_APPS`` of your project or something like that.


Usage
=====

That's how did you work with generic relations before:

.. code:: python

    # models.py
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    from django.db import models

    class Post(models.Model):
        pass

    class Image(models.Model):
         content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
         object_id = models.IntegerField()
         content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    # Example of filtering
    post = Post.objects.get(pk=1)
    images = Image.objects.filter(
        content_type=ContentType.objects.get_for_object(post),
        object_id=post.id
    )

Looks verbose a bit, yep? Let's rewrite this with ``django-generic-helpers``

.. code:: python

    # models.py
    from django.db import models
    from generic_helpers.fields import GenericRelationField

    class Post(models.Model):
        pass

    class Image(models.Model):
         content_object = GenericRelationField()

    # Example of filtering
    post = Post.objects.get(pk=1)
    images = Image.objects.filter(content_object=post)

Personally, I found it much simpler and cleaner.

Features the application provides:

* Creating an arbitrary number of generic relation fields, both required and optional;
* Providing custom names for ``content_type`` and ``object_id`` columns
* You can define a whitelist (or a black one) of models that could (not) be written into the field

Please, follow up the documentation for details.

Contributing
============

* If you found a bug, feel free to drop me `an issue on the repo <https://github.com/marazmiki/django-generic-helpers/issues/new>`_;
* Implemented a new feature could be useful? `Create a PR <https://github.com/marazmiki/django-generic-helpers/compare>`_!

A few words if you plan to send a PR:

* Please, write tests!
* Follow `PEP-0008 <https://www.python.org/dev/peps/pep-0008/>`_ codestyle recommendations.
* When pushing, please wait while `Travis CI <https://travis-ci.org/marazmiki/django-generic-helpers>`_ will finish his useful work and complete the build. And if the build fails, please fix the issues before PR
* And of course, don't forget to add yourself into the `authors list <https://github.com/marazmiki/django-generic-helpers/blob/master/docs/authors.rst>`_ ;)

License
=======

The license is MIT.
