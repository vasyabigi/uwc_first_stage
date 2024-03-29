from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from smart_selects.db_fields import ChainedForeignKey
from core.decorators import select_related_required
from core.models import BaseManager, QuerysetHelpers, WithCachedAllMethodManager
from sorl.thumbnail import ImageField


class CategoryQueryset(models.query.QuerySet, QuerysetHelpers):
    DEFAULT_SELECT_RELATED = ('parent',)


class CategoryManager(BaseManager):
    def get_query_set(self):
        return CategoryQueryset(self.model, using=self._db)

    def root_categories(self):
        q = self.published()\
            .filter(parent__isnull=True)\
            .prefetch_related('subcategories')
        return q


class Category(MPTTModel):
    # TODO: Published categories?
    # TODO: Position
    name = models.CharField(_('Category name'), max_length=150)
    slug = models.SlugField(_('Category permalink'), unique=True)
    parent = TreeForeignKey(
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

    class MPTTMeta:
        order_insertion_by = ['name']

    @models.permalink
    def get_absolute_url(self):
        return 'category-details', (self.slug,)


class ProductQueryset(models.query.QuerySet, QuerysetHelpers):
    DEFAULT_SELECT_RELATED = ('provider', 'category', 'category_parent')

    def with_variants(self):
        """ Prefetch variants of product """
        return self.prefetch_related('variants')

    def prefeth_parameters(self):
        return self.prefetch_related(
            'parameters',
            'parameters__parameter',
            'parameters__value'
        )

    def for_view(self, **kwargs):
        """
            Return queryset which is ready for a view
            (with all required related records and prefetched)
        """

        q = self.published()\
            .with_related()\
            .prefeth_parameters()\
            .filter(**kwargs)

        return q


class ProductManager(BaseManager):
    def get_query_set(self):
        return ProductQueryset(self.model, using=self._db)


class Product(models.Model):
    provider = models.ForeignKey('providers.Provider', related_name='products')
    category = models.ForeignKey(Category, related_name="products")
    parent = models.ForeignKey('self', verbose_name=_('Variant'),
        null=True, blank=True, related_name='variants')
    name = models.CharField(_('Product name'), max_length=120)
    slug = models.SlugField(_('Product permalink'), unique=True)
    description = models.TextField(_('Description'))
    published = models.BooleanField(_("Product is published"), default=False)

    created = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def __unicode__(self):
        return u'%s' % self.name

    @select_related_required('variants')
    def get_variants(self):
        """ Get variants of current product"""
        return self.variants or []

    @select_related_required('parameters', 'parameters__value')
    def get_short_specifications(self):
        specifications = ' / '.join([unicode(param.value) for param in self.parameters])
        return specifications

    @models.permalink
    def get_absolute_url(self):
        return 'product-details', (self.category.slug, self.slug)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images")
    is_main_image = models.BooleanField(default=False)
    image = ImageField(upload_to='images/', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.product


class ParameterManager(BaseManager):
    def filter_by_category(self, category):
        return self.get_query_set().filter(
            related_categories__category=category
        )


class Parameter(models.Model):
    name = models.CharField(_('Parameter Name'), max_length=120)

    objects = ParameterManager()
    simple_cached = WithCachedAllMethodManager()

    def __unicode__(self):
        return u'%s' % self.name


class ParameterValue(models.Model):
    parameter = models.ForeignKey(Parameter, related_name='values')
    value = models.CharField(max_length=120)

    def __unicode__(self):
        return u'%s' % self.value


class CategoryParameter(models.Model):
    """
        Parameters that we can use for describe product of category.
        e.g Display Size, Hdd, ...
    """
    category = models.ForeignKey(Category, related_name='parameters')
    parameter = models.ForeignKey(Parameter, related_name='related_categories')

    # simple_cached = WithCachedAllMethodManager()

    class Meta:
        unique_together = (('category', 'parameter'),)

    @select_related_required('parameter')
    def __unicode__(self):
        return u'%s' % (self.parameter.name,)


class ProductParameter(models.Model):
    """
        Parameter Of Product
    """
    product = models.ForeignKey(Product, related_name='parameters')
    parameter = models.ForeignKey(Parameter, related_name='related_product_parameters')
    value = ChainedForeignKey(
        ParameterValue,
        chained_field="parameter",
        chained_model_field="parameter",
        show_all=False,
        auto_choose=True
    )

    class Meta:
        unique_together = (('product', 'parameter'), )

    @select_related_required('value')
    def __unicode__(self):
        return u'%s' % self.value
