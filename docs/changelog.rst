1.0.1
-----

* A bugfix: don't change a customized manager with default django's one

1.0.0
-----

* A new declarative way to add generic relation fields to your model: any number or generic relation, any field name(s);
* Ability to add a generic relation for a restricted set of models. You can either enumerate all allowed models or all denied ones;
* An alternative way to add these fields: with a decorator (actually, it's not a new feature, just saved from unpublished release);
* The ``ct`` helper now caches own results;
* Added support for Python 3.6;
* Added support for Python 3.7;
* Added Django 2.0 and 2.1 support;
* Removed support for Python 3.3 and older;
* Removed support for Django 1.10 and older


0.3.7
-----

* Update django head version

0.3.6
-----

* Update django head version

0.3.5
-----

* Add CHANGELOG.rst into manifest


0.3.4
-----
* Remove deprecation warning

0.3.3
-----

* Moved the **ct** shortcut into **utils** module

0.3.2
-----

* Added CHANGELOG :)
* Added Python 3.4x support;
* Dropped Python 3.2x support;
* Improved code styling with pep8;
* Wheel available;
* Coverage support;
* Updated Django head version;
* Fix 0.3.1 install bug (import six from django).
