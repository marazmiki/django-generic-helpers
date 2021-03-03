from django.core import checks
from django.db import models


def check_field_type(field):
    if not isinstance(field.gr_opts['fk_field_type'], models.Field):
        return [
            checks.Error(
                msg=(
                    'if you need to change a foreign key field '
                    'type (e.g. UUID), you must provide a field '
                    'instanced object.'
                ),
                hint=(
                    'You should provide either "allow_content_types" '
                    'parameter, or "deny_content_types" one. Or, if '
                    'you don\'t need any limitation, just miss '
                    'this parameter.'
                ),
                obj=field,
                id='generic_helpers.E002',
            )
        ]
    else:
        return []


def check_limit_choices(field):
    if all((
            field.gr_opts['allow_content_types'],
            field.gr_opts['deny_content_types']
    )):
        return [
            checks.Error(
                msg=(
                    'Wrong generic relation limits specified: you\'ve '
                    'provided both "allow" and "deny" list.'
                ),
                hint=(
                    'You should provide either "allow_content_types" '
                    'parameter, or "deny_content_types" one. Or, if '
                    'you don\'t need any limitation, just miss '
                    'this parameter.'
                ),
                obj=field,
                id='generic_helpers.E001',
            )
        ]
    else:
        return []
