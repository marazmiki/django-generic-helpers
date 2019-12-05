try:
    from django.utils import six
    PY2 = six.PY2
    PY3 = six.PY3
except ImportError:
    PY3 = True
    PY2 = False
