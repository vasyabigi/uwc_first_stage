from haystack import indexes
from products.models import Product


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Product
