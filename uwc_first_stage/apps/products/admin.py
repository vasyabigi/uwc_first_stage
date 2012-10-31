from sorl.thumbnail.admin import AdminImageMixin
from django.contrib import admin
from models import Category, Product, Parameter, CategoryParameter, ParameterValue, ProductParameter, ProductImage
from forms import ProductImageInlineFormset


class ProductImageInline(AdminImageMixin, admin.TabularInline):
    model = ProductImage
    formset = ProductImageInlineFormset


class ProductParameterInline(admin.StackedInline):
    """
        Adds ability to add/change parameters on product page
    """
    model = ProductParameter
    # What's it for?
    # form = ProductParameterForm

    def get_formset(self, *args, **kwargs):
        formset = super(ProductParameterInline, self).get_formset(*args, **kwargs)
        # Override querieset of parameters (caching ModelChoiceField)
        formset.form.base_fields['parameter'].queryset = Parameter.simple_cached.all()
        return formset

    def queryset(self, request):
        q = super(ProductParameterInline, self).queryset(request)
        return q.select_related('parameter', 'value')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    fields = ('provider', 'category', 'name', 'description', 'slug', 'published')
    inlines = (
        ProductParameterInline,
        ProductImageInline,
    )

    class Media:
        # Managing categories and related parameters
        js = ('js/admin/product_parameter_choices.js',)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        # Add category and parameters data to javascript context
        # TODO: Remove this queries and do it ajax.
        category_parameters = CategoryParameter.objects\
            .filter(category__published=True)\
            .order_by('category')\
            .values_list('category', 'parameter')
        # Categories and parameters
        category_parameters_dict = {}
        for cat, param in category_parameters:
            category_parameters_dict.setdefault(cat, []).append(param)

        parameter_values = ParameterValue.objects\
            .all()\
            .values_list('parameter', 'id')\
            .order_by('parameter')
        # Parameters and values
        parameters_dict = {}
        for param, val in parameter_values:
            parameters_dict.setdefault(param, []).append(val)

        request.javascript_settings.update({
            'adminProductPage': {
                'categoryParameters': category_parameters_dict,
                'parameterValues': parameters_dict
            }
        })

        return super(ProductAdmin, self).render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)


class CategoryParameterInline(admin.StackedInline):
    """
        Adds Ability to add/change parameters on Category add/change view
    """
    model = CategoryParameter

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CategoryParameterInline, self).get_formset(request, obj=obj, **kwargs)
        ids = []

        if obj and obj.id:
            ids.append(obj.id)
            if obj.parent:
                ids.append(obj.parent.id)

        # Override queryset of parameters. Shows only instance and parent parameters
        if ids:
            formset.form.base_fields['parameter'].queryset = Parameter.simple_cached.filter(
                related_categories__category__in=ids
            ).distinct()

        return formset

    def queryset(self, request):
        q = super(CategoryParameterInline, self).queryset(request)
        return q.select_related('parameter', 'category', 'category__parent')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CategoryParameterInline,)


class ParameterValueInline(admin.StackedInline):
    model = ParameterValue

    def queryset(self, request):
        q = super(ParameterValueInline, self).queryset(request)
        return q.select_related('parameter')


class CategoryInline(admin.StackedInline):
    """
        Select Category from Add/Change Parameter page
    """
    model = CategoryParameter
    extra = 1
    max_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CategoryInline, self).get_formset(request, obj, **kwargs)

        # Prepopulate category if we have id in get request
        try:
            category_id = int(request.GET.get('category'))
        except TypeError:
            category_id = None

        if category_id:
            formset.form.base_fields['category'].queryset = formset.form.base_fields['category'].queryset.filter(id=category_id)
            formset.form.base_fields['category'].initial = category_id

        return formset


class ParameterAdmin(admin.ModelAdmin):
    inlines = [
        ParameterValueInline,
        CategoryInline
    ]


admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
