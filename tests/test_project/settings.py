SECRET_KEY = '****'
DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'generic_helpers',
    'test_project',
]

MIDDLEWARE = []
MIDDLEWARE_CLASSES = MIDDLEWARE  # The same for older django versions

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
