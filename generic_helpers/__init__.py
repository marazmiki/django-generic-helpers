# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import sys


VERSION = (0, 3, 6)


def get_version():
    PY3 = sys.version_info[0] == 3

    if PY3:
        text_type = str
    else:
        text_type = unicode    # NOQA
    return '.'.join(map(text_type, VERSION))


__author__ = 'Mikhail Porokhovnichenko <marazmiki@gmail.com>'
__version__ = get_version()
