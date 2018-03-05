======================
django-generic-helpers
======================

.. image:: https://badge.fury.io/py/django-generic-helpers.png
    :target: http://badge.fury.io/py/django-generic-helpers
    
.. image:: https://travis-ci.org/marazmiki/django-generic-helpers.png?branch=master
        :target: https://travis-ci.org/marazmiki/django-generic-helpers

.. image:: https://coveralls.io/repos/marazmiki/django-generic-helpers/badge.png?branch=master
  :target: https://coveralls.io/r/marazmiki/django-generic-helpers?branch=master

.. image:: https://img.shields.io/pypi/dm/django-generic-helpers.svg
        :target: https://pypi.python.org/pypi/django-generic-helpers

.. image:: https://img.shields.io/pypi/wheel/django-generic-helpers.svg
    :target: https://pypi.python.org/pypi/django-generic-helpers/
    :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/django-generic-helpers.svg
    :target: https://pypi.python.org/pypi/django-generic-helpers/
    :alt: Supported Python versions


This app provides some snippets (such as abstract models and managers
with some useful methods) to simplyfy creation of another pluggable apps.

The license is MIT.


Installation
============

.. code:: bash

    pip install django-generic-helpers

After you can add the `generic_helpers` app into your `INSTALLED_APPS`. If you aren't
want to run test, you can skip this step.

Usage
=====

To use this app, just import GenericRelationModel class from
generic_helpers.models package and inherit your model from it:

.. code:: python

    from django.db import models
    from generic_helpers.models import GenericRelationModel

    class MyModel(GenericRelationModel):
        title = models.CharField(max_length=255)

Now MyModel class has content_object attribute and you can create MyModel
instances using generic relation:

.. code:: python

    >>> from django.contrib.auth.models import User
    >>> user = User.objects.get(pk=1)
    >>>
    >>> my_model = MyModel.objects.create(title='title',
    ...                                   content_object=user)
    >>>

In this example how you can see we have used User.

Also your model manager has a get_for_object method for quick filtering by
content_object complex field:

.. code:: python


    >>> from django.contrib.auth.models import User
    >>> user = User.objects.get(pk=1)
    >>>
    >>> models_for_user = MyModel.objects.get_for_object(user)
    >>>

Contributing
============

If you've found a bug, implemented a feature and think it is useful, or you've
own pluggable app and want to use django-generic-helpers in it, then please
consider contributing. Patches, pull requests or just suggestions are welcome!
