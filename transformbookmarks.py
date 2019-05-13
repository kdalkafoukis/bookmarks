#!/usr/bin/env python3.7

import requests
import html2text
import re

from getbookmarks import getBookmarks
# from getbookmarks import printBookmarks

def filteredText(url): #take a website and tranform it to text
    r = requests.get(url)   #make the request

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True

    text = text_maker.handle(r.text)    #html to text
    splitted_text = text.split()

    final_text = []
    for i in splitted_text:             #clear the text
        temp = re.sub("[^A-Za-z]", "", i)
        if (temp != ''):
            final_text.append(temp)

    return " ".join(final_text)         #make the array text again

bookmarks = getBookmarks()

text = filteredText(bookmarks[0])
print(text)

# for bookmark in bookmarks:
#     text = filteredText(bookmark)
#     print(text)
