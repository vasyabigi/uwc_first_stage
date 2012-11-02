import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError
from products.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get('http://www.etsy.com/browse/women?ref=fp_ln_new_women')
        soup = BeautifulSoup(r.text)

        # Parent categories
        results = list()
        soup_list = soup.select('#feed-new-nav li')[2:]
        for r in soup_list:
            # create category
            name = r.text.replace(' ', '').replace('\n', '')
            category, created = Category.objects.get_or_create(
                name=name,
                slug=slugify(name),
            )
            results.append({
                'link': r.a.get('href'),
                'category': category.slug
            })

        # Child categories
        for item in results:
            r = requests.get(item['link'])
            soup = BeautifulSoup(r.text)
            item_results = list()
            soup_list = soup.select('#feed-new-nav li')
            for r in soup_list:
                # create category
                name = r.text.replace(' ', '').replace('\n', '')
                try:
                    category, created = Category.objects.get_or_create(
                        name=name,
                        slug=slugify(name),
                        parent=Category.objects.get(slug=item['category'])
                    )
                except IntegrityError:
                    pass
                else:
                    item_results.append({
                        'link': r.a.get('href')
                    })
