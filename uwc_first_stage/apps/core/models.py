from django.db import models
import os


class QuerysetHelpers(object):
    """
        Mixin for Queryset that provides good and helpful methods
    """

    DEFAULT_SELECT_RELATED = None
    DEFAULT_PREFETCH_RELATED = None

    def published(self):
        return self.filter(published=True)

    def with_related(self):
        """
            Default select/prefetch related
        """
        q = self
        if self.DEFAULT_SELECT_RELATED:
            q = self.select_related(*self.DEFAULT_RELATED)

        if self.DEFAULT_PREFETCH_RELATED:
            q = self.select_related(*self.DEFAULT_PREFETCH_RELATED)

        return q


class BaseManager(models.Model):
    def __getattr__(self, attr, *args):
        """
            Looks method also in queryset
        """
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


def get_upload_path(instance, name):
    try:
        name = name.encode('utf-8')
    except Exception:
        pass

    return os.path.join(instance.__class__.__name__.lower(), str(instance.slug), name)
