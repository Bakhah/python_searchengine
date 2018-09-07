from pydash import filter_, map_, sorted_uniq, pull_all, get
from string import punctuation
from data.constants import empty_words


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
    without_empty_words = pull_all(lowered_list, empty_words)
    res = {}
    for word in without_empty_words:
        if get(res, word):
            res[word] += 1
        else:
            res[word] = 1
    return res


def no_punc(s):
    return ''.join(c for c in s if c not in punctuation)
