def memoize_method(func):
    """
        Call the object method just once for a args set and memoize the result
    """
    key = func.__name__

    def inner(self, *args, **kwargs):
        try:
            cache = self._mm
        except AttributeError:
            cache = {}
            self._mm = cache

        key_args = key + (str(args) if args else '') + (str(kwargs) if kwargs else '')
        try:
            res = cache[key_args]
        except KeyError:
            res = func(self, *args, **kwargs)
            cache[key_args] = res

        return res
    return inner


def select_related_required(*fields):
    """
       Checks, that select_related was used for given fields
    """
    def wrap(func):
        def _wrap_f(self, *args, **kwargs):
            cache_attribute_name = '_%s_cache'

            def _check_cache(obj, field):
                if not hasattr(obj, cache_attribute_name % field):
                    raise Exception('Use select related for this fields, bitch: %s' % str(fields))

            def _reducer(obj, field):
                next_obj = None
                if obj:
                    cache_attr = cache_attribute_name % field
                    _check_cache(obj, field)
                    next_obj = getattr(obj, cache_attr)

                return next_obj

            for field in fields:
                if '__' in field:
                    reduce(_reducer, field.split('__'), self)
                else:
                    _check_cache(self, field)

            return func(self, *args, **kwargs)

        return _wrap_f

    return wrap
