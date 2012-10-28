from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import BaseManager, QuerysetHelpers, get_upload_path


class Category(models.Model):
    name = models.CharField(_('Category name'), max_length=150)
    parent = models.ForeignKey(
        'self',
        related_name='subcategories',
        limit_choices_to={'parent__isnull': True},
        null=True,
        blank=True
    )

    def __unicode__(self):
        return u'%s' % self.name


class ProductQueryset(models.query.QuerySet, QuerysetHelpers):
    DEFAULT_SELECT_RELATED = ('provider', 'category', 'category_parent')


class ProductManager(BaseManager):
    def get_query_set(self):
        return ProductQueryset()


class Product(models.Model):
    provider = models.ForeignKey('providers.Provider', related_name='products')
    category = models.ForeignKey(Category)

    name = models.CharField(_('Product name'), max_length=120)
    slug = models.SlugField(_('Product permalink'), unique=True)
    description = models.TextField(_('Description'))
    image = models.ImageField(
        _('Image'),
        null=True,
        blank=True,
        upload_to=get_upload_path
    )
    published = models.BooleanField(_("Product is published"),default=False)

    created = models.DateTimeField(auto_now_add=True)

    object = ProductManager()

    def __unicode__(self):
        return u'%s' % self.name
