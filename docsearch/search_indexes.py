from haystack import indexes

from docsearch import models


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    township = indexes.CharField(model_attr='township')
    section = indexes.CharField(model_attr='section', null=True)
    range = indexes.CharField(model_attr='range')

    def get_model(self):
        return models.Book
