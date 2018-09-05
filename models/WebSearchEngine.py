from pydash import intersection, union
import pickle


class WebSearchEngine():
    """docstring for WebSearchEngine"""
    def __init__(self):
        self.count = 0
        self.indexed_urls = []
        self.search_dict = {}

    def __repr__(self):
        return str(self.__dict__)

    def index(self, webpage):
        for word in webpage.desc_words:
            key_value = self.search_dict.get(word)
            if not key_value:
                self.search_dict[word] = []
            self.search_dict[word].append(webpage.url)
        self.indexed_urls.append(webpage.url)
        pickle.dump(self, open("save.p", "wb"))

    def single_search(self, query):
        return self.search_dict.get(query)

    def multiple_search(self, word_list, is_conjunctive):
        first_search = True
        urls = []
        for word in word_list:
            if is_conjunctive:
                if first_search:
                    urls = union(urls, self.search_dict.get(word))
                    first_search = False
                else:
                    urls = intersection(urls, self.search_dict.get(word))
            else:
                urls = union(urls, self.search_dict.get(word))
        return urls

    def all_urls(self):
        return self.indexed_urls

