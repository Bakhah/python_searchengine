#!/usr/bin/python3

import urllib
import sys
from bs4 import BeautifulSoup


def download(url):
    parsed_url = urllib.parse.urlparse(url)
    res = ""
    try:
        with urllib.request.urlopen(parsed_url.geturl()) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'lxml')
            found = False

            for meta in soup.find_all('meta'):
                if meta.get("property") == 'og:description':
                    found = True
                    return meta.get('content')

            if not found:
                return res
    except:
        return res


def downloadFile(file):
    try:
        with open(sys.argv[1], "r") as f:
            for line in f:
                description = download(line)
                print(description)
    except FileNotFoundError:
        print("Ce fichier n'existe pas")


# if len(sys.argv) == 2:
#     downloadFile(sys.argv[1])
# else:
#     url = input('Saisir un url :\n')
#     description = download(url)
#     print(description)


