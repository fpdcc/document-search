from haystack.query import SearchQuerySet

from docsearch.inputs import FuzzyAutoQuery


class FuzzySearchQuerySet(SearchQuerySet):
    """A SearchQuerySet modified to run auto_query with fuzzy search."""
    def auto_query(self, query_string, fieldname='content'):
        """Override auto_query to provide fuzzy search support."""
        # This is the only line that has been adjusted, to make sure that
        # all queries are processed as fuzzy queries.
        kwargs = {fieldname: FuzzyAutoQuery(query_string)}
        return self.filter(**kwargs)
