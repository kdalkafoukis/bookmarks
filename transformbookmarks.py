#!/usr/bin/env python3.7

import requests
import html2text
import re

from getbookmarks import getBookmarks
# from getbookmarks import printBookmarks

def filteredText(url): #take a website and tranform it to text
    try:
        r = requests.get(url,verify= False)   #make the request
        # r = requests.get(url)   #make the reques

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
    except ( requests.exceptions.RequestException) as e:
        pass

bookmarks = getBookmarks()

for bookmark in bookmarks:
    
    text = filteredText(bookmark)
    print(text)