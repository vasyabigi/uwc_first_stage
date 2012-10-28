from django.shortcuts import render
from products.models import Category


def home(request):
    categories = Category.objects.root_categories()
    context = {
        'categories': categories
    }
    return render(request, 'core/home.html', context)
