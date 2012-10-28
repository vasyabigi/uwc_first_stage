from django.contrib import admin

from models import Category, Product
from products.models import Parameter, CategoryParameter, ParameterValue

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    fields = ('provider', 'category', 'name', 'description', 'image','slug', 'published')
    

class CategoryParameterInline(admin.StackedInline):
    model = CategoryParameter


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryParameterInline
    ]


class ParameterValueInline(admin.StackedInline):
    model = ParameterValue

    def queryset(self, request):
        return super(ParameterValueInline, self).queryset(request).select_related('parameter')


class ParameterAdmin(admin.ModelAdmin):
    inlines = [
        ParameterValueInline
    ]



admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)