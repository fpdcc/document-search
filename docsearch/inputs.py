import re

from haystack.inputs import BaseInput, Exact, Not


class FuzzyClean(BaseInput):
    """An input type for sanitizing untrusted input and making it fuzzy.

    Adapted from:
    https://github.com/django-haystack/django-haystack/blob/ea3f8c961934e8871b89881d7fab09e038191899/haystack/inputs.py#L51-L60
    """
    input_type_name = 'fuzzy_clean'

    def prepare(self, query_obj):
        query_string = super().prepare(query_obj)
        cleaned_q = query_obj.clean(query_string)
        # This is the only line that has been changed, to append tildes (fuzzy
        # search characters) to the end of every cleaned term.
        return ' '.join(term + '~' for term in cleaned_q.split())


class FuzzyAutoQuery(BaseInput):
    """
    A fork of the Haystack AutoQuery class that handles common user queries.
    In addition to cleaning all tokens, it handles double quote bits as
    exact matches and terms with '-' in front as NOT queries, and also supports
    fuzzy search.

    Adapted from:
    https://github.com/django-haystack/django-haystack/blob/ea3f8c961934e8871b89881d7fab09e038191899/haystack/inputs.py#L95-L134
    """
    input_type_name = 'fuzzy_auto_query'
    post_process = False
    exact_match_re = re.compile(r'"(?P<phrase>.*?)"')

    def prepare(self, query_obj):
        query_string = super().prepare(query_obj)
        exacts = self.exact_match_re.findall(query_string)
        tokens = []
        query_bits = []

        for rough_token in self.exact_match_re.split(query_string):
            if not rough_token:
                continue
            elif rough_token not in exacts:
                # We have something that's not an exact match but may have more
                # than one word in it.
                tokens.extend(rough_token.split(' '))
            else:
                tokens.append(rough_token)

        for token in tokens:
            if not token:
                continue
            if token in exacts:
                query_bits.append(Exact(token, clean=True).prepare(query_obj))
            elif token.startswith('-') and len(token) > 1:
                query_bits.append(Not(token[1:]).prepare(query_obj))
            else:
                # This is the only line that has been adjusted, to make sure
                # non-exact non-not search terms are fuzzy.
                query_bits.append(FuzzyClean(token).prepare(query_obj))

        return ' '.join(query_bits)
