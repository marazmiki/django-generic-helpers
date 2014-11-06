#!/usr/bin/env python
# coding: utf-8

from django import get_version
from django.conf import settings

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


settings.configure(
    INSTALLED_APPS=(
        'django.contrib.contenttypes',
        'generic_helpers',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':MEMORY:'
        }
    },
)


def main():
    from django.test.utils import get_runner
    import django

    if hasattr(django, 'setup'):
        django.setup()

    find_pattern = 'generic_helpers'

    if get_version() >= '1.6':
        find_pattern = 'generic_helpers.tests'

    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failed = test_runner.run_tests([find_pattern])

    if not failed:
        settings.GENERIC_HELPERS_USE_TEXT_OBJECT_PK = False
        test_runner = get_runner(settings)(verbosity=2, interactive=True)
        failed = test_runner.run_tests([find_pattern])

    sys.exit(failed)


if __name__ == '__main__':
    main()
