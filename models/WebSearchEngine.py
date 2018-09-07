from pydash import intersection_with, union_with, get, for_in, order_by
import pickle
from models.bcolors import bcolors


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
            if not get(self.search_dict, word):
                self.search_dict[word] = []
            self.search_dict[word].append({
                'url': webpage.url,
                'count': count
            })

        for_in(webpage.desc_words, parse_desc)
        self.indexed_urls.append(webpage.url)
        pickle.dump(self, open("save.p", "wb"))

    def single_search(self, query):
        self.count += 1
        search = order_by(get(self.search_dict, query), ['count'], True)
        self.print_list(search, True)

    def multiple_search(self, word_list, is_conjunctive):
        comparator = lambda a, b: a['url'] == b['url']

        self.count += 1
        first_search = True
        urls = []
        for word in word_list:
            if is_conjunctive:
                if first_search:
                    urls = union_with(urls, get(self.search_dict, word), comparator)
                    first_search = False
                else:
                    urls = intersection_with(urls, get(self.search_dict, word), comparator)
            else:
                urls = union_with(urls, get(self.search_dict, word), comparator)
        self.print_list(urls, False)

    # def deindex(self, url):
    #     # if url in self.indexed_urls:
    #     #     # pull(self.indexed_urls, url)
    #     # else:
    #     #     print("Cet url n'est pas indexé\n")

    def all_urls(self):
        return self.indexed_urls

    def print_list(self, list, with_occurence):
        if not list:
            print(bcolors.FAIL, "\n\n\tAucun résultat...")
        else:
            print(bcolors.OKGREEN, "\n", len(list), " résultats : \n")
            for i, item in enumerate(list):
                print("\t", i + 1, ") ", item['url'], " (",item['count'],' fois)')
        print("\n", bcolors.ENDC)

