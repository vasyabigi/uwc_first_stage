from django.conf.urls.defaults import patterns, url
from products.views import category_details, product_details


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', category_details, name="category-details"),
    url(r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/$', product_details, name="product-details"),
)
