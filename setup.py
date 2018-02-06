#!/usr/bin/env python
# coding: utf-8

import sys
from setuptools import setup
from setuptools.command.test import test


class TestCmd(test):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to pytest")
    ]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        import shlex
        sys.exit(pytest.main(shlex.split(self.pytest_args)))


setup(cmdclass={
    'test': TestCmd,
})
