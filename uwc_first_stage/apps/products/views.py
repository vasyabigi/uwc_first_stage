from products.forms import ParameterFilteringForm
from products.models import Category, Product
from django.shortcuts import render, get_object_or_404


def category_details(request, slug):
    category = get_object_or_404(Category, slug=slug)

    parameter_filtering_form = ParameterFilteringForm(
        category,
        data=request.GET or None
    )

    if request.GET:
        products = parameter_filtering_form.get_products()
    else:
        products = category.products.for_view()

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'products/category-details.html', context)


def product_details(request, category_slug, product_slug):
    product = get_object_or_404(
        Product.objects.for_view(),
        slug=product_slug
    )

    category = product.category

    context = {
        'category': category,
        'product': product
    }

    return render(request, 'products/product-details.html', context)
