from django.db.models import Manager


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
        def _wrap_f(model_instance, *args, **kwargs):
            cache_attribute_name = '_%s_cache'

            def _check_cache(obj, field_name):
                field = getattr(obj, field_name)

                if isinstance(field, Manager):
                    # Check prefetch related
                    q = field.all()
                    if not q._prefetch_done:
                        raise Exception('Use select prefetch_related for this field, bitch: %s' % str(field_name))
                    return q[0] if len(q) else None
                else:
                    cache_attr = cache_attribute_name % field_name
                    if not hasattr(obj, cache_attribute_name % field_name):
                        raise Exception('Use select related for this fields, bitch: %s' % str(fields))
                    return getattr(obj, cache_attr)

            def _reducer(obj, field):
                next_obj = None
                if obj:
                    cache_attr = cache_attribute_name % field
                    next_obj = _check_cache(obj, field)

                return next_obj

            for field in fields:
                reduce(_reducer, field.split('__'), model_instance)

            return func(model_instance, *args, **kwargs)

        return _wrap_f

    return wrap
