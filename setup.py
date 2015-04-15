#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os


version = __import__('generic_helpers').get_version()


DIR = os.path.dirname(__file__)
DOWNLOAD_URL = ('https://github.com/marazmiki/django-generic-helpers/'
                'archive/master.zip')


CLASSIFIERS = [
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Framework :: Django'
]


def long_description():
    """
    Returns package long description from README
    """
    def read(what):
        with open(os.path.join(DIR, '%s.rst' % what)) as fp:
            return fp.read()

    return "{README}\n\n{CHANGELOG}".format(README=read('README'),
                                            CHANGELOG=read('CHANGELOG'))


setup(name='django-generic-helpers',
      author='Mikhail Porokhovnichenko <marazmiki@gmail.com>',
      version=version,
      author_email='marazmiki@gmail.com',
      url='https://github.com/marazmiki/django-generic-helpers',
      download_url=DOWNLOAD_URL,
      description=('The small frameworks that helps to write '
                   'reusable django apps with generic relations'),
      long_description=long_description(),
      license='MIT license',
      platforms=['OS Independent'],
      classifiers=CLASSIFIERS,
      install_requires=[
          'Django>=1.5',
      ],
      tests_require=[],
      test_suite='tests.main',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
