class generic_relation:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        def inner(*args, **kwargs):
            return func(self.param, *args, **kwargs)
        return inner
