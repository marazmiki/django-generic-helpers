from .fields import GenericRelationField


def generic_relation(*args, **kwargs):
    model_class = None

    if len(args) == 1 and callable(args[0]):
        model_class = args[0]

    def inner(model_class):
        gr_name = kwargs.pop('gr_field', 'content_object')

        ct_field = kwargs.pop('ct_field', None)
        fk_field = kwargs.pop('fk_field', None)

        # Customize the content-type field name
        if not ct_field:
            ct_field = '{0}_content_type'.format(gr_name)
            if gr_name == 'content_object':
                ct_field = 'content_type'

        # Customize the object id field name
        if not fk_field:
            fk_field = '{0}_object_id'.format(gr_name)
            if gr_name == 'content_object':
                fk_field = 'object_id'

        # Attaching a generic relation field to the model class
        GenericRelationField(
            ct_field=ct_field,
            fk_field=fk_field,
        ).contribute_to_class(model_class, gr_name)

        return model_class

    return inner(model_class) if model_class else inner
