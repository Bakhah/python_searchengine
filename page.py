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
        for i, item in enumerate(list):
            print("\t", i + 1, ") ", item)
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
    mode = input("1) Indexer un nouvel url\n2) Désindexer un url existant\n3) Effectuer une recherche\n4) Voir tous les urls indexés\n\nChoix : ")

    if mode == "1":
        url_to_index = input("Saisissez un url à indexer : ")
        index_url(url_to_index, 1)

    if mode == "2":
        url_to_deindex = input("Saisissez un url à désindexer : ")
        search_engine.deindex(url_to_deindex)

    if mode == "3":
        query = input("Rechercher : ")
        is_conjunctive = False
        splitted_words = query.split()
        results = []

        if len(splitted_words) > 1:
            answer = input("Recherche conjonctive ? O/N : ")
            if answer == "O":
                is_conj = True
            results = search_engine.multiple_search(splitted_words, is_conj)

        else:
            results = search_engine.single_search(splitted_words[0])

        print_list(results)

    if mode == '4':
        for url in search_engine.all_urls():
            print(url)
        print('\n')

    pickle.dump(search_engine, open("save.p", "wb"))

