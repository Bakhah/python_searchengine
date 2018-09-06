from pydash import intersection, union, get, for_in
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

        def parse_desc(count, word):
            if get(self.search_dict, word):
                self.search_dict[word].append({webpage.url: count})
            else:
                self.search_dict[word] = []
                self.search_dict[word].append({webpage.url: count})

        for_in(webpage.desc_words, parse_desc)
        self.indexed_urls.append(webpage.url)
        pickle.dump(self, open("save.p", "wb"))

    def single_search(self, query):
        self.count += 1
        return get(self.search_dict, query + ".urls")

    def multiple_search(self, word_list, is_conjunctive):
        self.count += 1
        first_search = True
        urls = []
        for word in word_list:
            if is_conjunctive:
                if first_search:
                    urls = union(urls, get(self.search_dict, word + ".urls"))
                    first_search = False
                else:
                    urls = intersection(urls, get(self.search_dict, word + ".urls"))
            else:
                urls = union(urls, get(self.search_dict, word + ".urls"))
        return urls

    # def deindex(self, url):
    #     # if url in self.indexed_urls:
    #     #     # pull(self.indexed_urls, url)
    #     # else:
    #     #     print("Cet url n'est pas indexé\n")


    def all_urls(self):
        return self.indexed_urls

