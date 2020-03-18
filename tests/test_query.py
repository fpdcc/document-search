from docsearch.query import FuzzySearchQuerySet


def get_fuzzy_auto_query(query_string):
    """Helper function to retrieve an auto_query from a FuzzySearchQuerySet."""
    return str(FuzzySearchQuerySet().auto_query(query_string).query)


def test_fuzzysearchqueryset_auto_query_appends_tildes():
    assert get_fuzzy_auto_query('cerm ak') == '(cerm~ ak~)'


def test_fuzzysearchqueryset_auto_query_exact_matches():
    assert get_fuzzy_auto_query('"cerm" ak') == '("cerm" ak~)'


def test_fuzzysearchqueryset_auto_query_exclude():
    assert get_fuzzy_auto_query('-cerm ak') == '(NOT cerm ak~)'
