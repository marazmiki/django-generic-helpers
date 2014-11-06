# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


VERSION = (0, 3, 2)


def get_version():
    return '.'.join(map(str, VERSION))


__author__ = 'Mikhail Porokhovnichenko <marazmiki@gmail.com>'
__version__ = get_version()
