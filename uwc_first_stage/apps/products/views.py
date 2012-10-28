from products.models import Category, Product
from django.shortcuts import render, get_object_or_404


def category_details(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {
        'category': category
    }
    return render(request, 'products/category-details.html', context)


def product_details(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug)
    context = {
        'category': category,
        'product': product
    }
    return render(request, 'products/product-details.html', context)
