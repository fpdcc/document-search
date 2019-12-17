from haystack.forms import FacetedSearchForm


class BaseSearchForm(FacetedSearchForm):
    def no_query_found(self):
        """If the user inputs no query, return all documents."""
        return self.searchqueryset.all()
