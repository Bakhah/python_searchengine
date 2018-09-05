#!/usr/bin/python3

import sys
from urllib.parse import urlparse
from models.WebPage import WebPage
from models.WebSearchEngine import WebSearchEngine
from models.bcolors import bcolors
from web import download


def print_list(list):
    if not list:
        print(bcolors.FAIL, "\n\n\tAucun résultat...")
    else:
        print(bcolors.OKGREEN, "\n", len(list), " résultats : \n")
        for item in list:
            print("\t", item)
    print("\n", bcolors.ENDC)


webpages = []
num_lines = sum(1 for line in open('urllist.txt'))
percent = 0.0
search_engine = WebSearchEngine()

with open("urllist.txt", "r") as f:
    for line in f:
        description = download(line)
        clean_line = urlparse(line.rstrip('\r\n'))
        search_engine.index(WebPage(clean_line.geturl(), description))
        percent += 100 / num_lines
        sys.stdout.write("     Indexation en cours... \r%d%%" % percent)
        sys.stdout.flush()
        if percent == 100:
            sys.stdout.flush()
            sys.stdout.write("    Indexation terminée\n\n")

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

