from pydash import filter_, map_, sorted_uniq
from string import punctuation


class WebPage(object):
    """docstring for ClassName"""
    def __init__(self, url, description):
        self.url = url
        self.description = description
        self.desc_words = parseDescription(description)

    def __repr__(self):
        return str(self.__dict__)


def parseDescription(description):
    list = description.split()
    no_small_words_list = filter_(list, lambda word: len(word) > 2)
    lowered_list = map_(no_small_words_list, lambda word: no_punc(word.lower()))
    unique_words_list = sorted_uniq(lowered_list)
    return unique_words_list


def no_punc(s):
    return ''.join(c for c in s if c not in punctuation)
