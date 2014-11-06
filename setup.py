#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os


version = __import__('generic_helpers').get_version()
readme = os.path.join(os.path.dirname(__file__), 'README.rst')


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django'
]

with open(readme) as fp:
    setup(
        name='django-generic-helpers',
        author='Mikhail Porokhovnichenko <marazmiki@gmail.com>',
        version=version,
        author_email='marazmiki@gmail.com',
        url='https://github.com/marazmiki/django-generic-helpers',
        download_url='https://github.com/marazmiki/django-generic-helpers/archive/master.zip',
        description='The small frameworks that helps to write reusable django apps',
        long_description=fp.read(),
        license='MIT license',
        platforms=['OS Independent'],
        classifiers=CLASSIFIERS,
        install_requires=[
            'Django>=1.3.1',
        ],
        tests_require=[],
        test_suite='tests.main',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False)
