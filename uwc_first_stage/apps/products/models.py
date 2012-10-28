from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.decorators import select_related_required

from core.models import BaseManager, QuerysetHelpers, get_upload_path


class CategoryManager(QuerysetHelpers):
    def root_categories(self, **kwargs):
        return self.published().filter(parent__isnull=True)


class Category(models.Model):
    # TODO: Published categories?
    # TODO: Position
    name = models.CharField(_('Category name'), max_length=150)
    slug = models.SlugField(_('Category permalink'), unique=True)
    parent = models.ForeignKey(
        'self',
        related_name='subcategories',
        limit_choices_to={'parent__isnull': True},
        null=True,
        blank=True
    )
    published = models.BooleanField(_("Category is published"), default=True)

    objects = CategoryManager()

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return 'category-details', (self.slug,)


class ProductQueryset(models.query.QuerySet, QuerysetHelpers):
    DEFAULT_SELECT_RELATED = ('provider', 'category', 'category_parent')

    def with_variants(self):
        """ Prefetch variants of product """
        return self.prefetch_related('variants')


class ProductManager(BaseManager):
    def get_query_set(self):
        return ProductQueryset()


class Product(models.Model):
    provider = models.ForeignKey('providers.Provider', related_name='products')
    category = models.ForeignKey(Category, related_name="products")
    parent = models.ForeignKey(
        'self',
        verbose_name=_('Variant'),
        null=True,
        blank=True,
        related_name='variants'
    )
    name = models.CharField(_('Product name'), max_length=120)
    slug = models.SlugField(_('Product permalink'), unique=True)
    description = models.TextField(_('Description'))
    image = models.ImageField(
        _('Image'),
        null=True,
        blank=True,
        upload_to=get_upload_path
    )
    published = models.BooleanField(_("Product is published"), default=False)

    created = models.DateTimeField(auto_now_add=True)

    object = ProductManager()

    def __unicode__(self):
        return u'%s' % self.name

    @select_related_required('variants')
    def get_variants(self):
        """ Get variants of current product"""
        return self.variants or []

    @models.permalink
    def get_absolute_url(self):
        return 'product-details', (self.category.slug, self.slug)


class Parameter(models.Model):
    name = models.CharField(_('Parameter Name'), max_length=120)


class ParameterValue(models.Model):
    parameter = models.ForeignKey(Parameter, related_name='values')
    value = models.CharField(max_length=120)

    @select_related_required('parameter')
    def __unicode__(self):
        return u'%s - %s' (unicode(self.parameter), self.value)


class CategoryParameter(models.Model):
    """
        Parameters that we can use for describe product of category.
        e.g Display Size, Hdd, ...
    """
    category = models.ForeignKey(Category, related_name='parameters')
    parameter = models.ForeignKey(Parameter, related_name='related_categories')

    class Meta:
        unique_together = (('category', 'parameter'),)

    def __unicode__(self):
        return u'%s' % self.name


class ParameterValue(models.Model):
    parameter = models.ForeignKey(Parameter, related_name='values')
    value = models.CharField(max_length=120)

    @select_related_required('parameter')
    def __unicode__(self):
        return u'%s - %s' (unicode(self.parameter), self.value)


class ProductParameter(models.Model):
    """
        Parameter Of Product
    """
    product = models.ForeignKey(Product, related_name='parameters')
    parameter = models.ForeignKey(Parameter, related_name='related_product_parameters')
    value = models.ForeignKey(ParameterValue)

    class Meta:
        unique_together = (('product', 'parameter'), )

    def __unicode__(self):
        return u'%s' % self.value
