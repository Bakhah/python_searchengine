#!/usr/bin/python3

import sys
from urllib.parse import urlparse
from models.WebPage import WebPage
from models.WebSearchEngine import WebSearchEngine
from models.bcolors import bcolors
from web import download
import pickle
import os.path

percent = 0.0


def print_list(list):
    if not list:
        print(bcolors.FAIL, "\n\n\tAucun résultat...")
    else:
        print(bcolors.OKGREEN, "\n", len(list), " résultats : \n")
        for item in list:
            print("\t", item)
    print("\n", bcolors.ENDC)


def look_for_something_to_index(search_engine):
    global percent
    urls_to_index = []
    with open("urllist.txt", "r") as f:
        for line in f:
            if line.rstrip('\r\n') not in search_engine.indexed_urls:
                urls_to_index.append(line)

    list_length = len(urls_to_index)
    for url in urls_to_index:
        index_url(url, list_length)


def index_url(line, num_lines):
    global percent
    description = download(line)
    clean_line = urlparse(line.rstrip('\r\n'))
    search_engine.index(WebPage(clean_line.geturl(), description))
    percent += 100 / num_lines
    sys.stdout.write("     Indexation en cours... \r%d%%" % percent)
    sys.stdout.flush()
    if percent == 100:
        sys.stdout.flush()
        sys.stdout.write("    Indexation terminée\n\n")


def index_all():
    global percent
    with open("urllist.txt", "r") as f:
        for line in f:
            index_url(line, num_lines)
    percent = 0.0


previous_state = os.path.exists("save.p")
webpages = []
num_lines = sum(1 for line in open('urllist.txt'))

if previous_state:
    search_engine = pickle.load(open("save.p", "rb"))
    look_for_something_to_index(search_engine)
else:
    search_engine = WebSearchEngine()
    index_all()


while True:
    query = input("Rechercher : ")
    is_conjunctive = False
    splitted_words = query.split()
    results = []

    if len(splitted_words) > 1:
        answer = input("Recherche conjonctive ? O/N : ")
        if answer == "O":
            is_conjunctive = True
        results = search_engine.multiple_search(splitted_words, is_conjunctive)

    else:
        results = search_engine.single_search(splitted_words[0])

    print_list(results)

