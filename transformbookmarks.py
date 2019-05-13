#!/usr/bin/env python3.7

# import requests
import urllib3
import html2text
import re
# import time

from getbookmarks import getBookmarks
# from getbookmarks import printBookmarks

http = urllib3.PoolManager()

def filteredText(url): #take a website and tranform it to text
    # r = requests.get(url,verify= False)   #make the request
    # r = requests.get(url)   #make the reques

    try:
        r = http.request('GET', url, retries=urllib3.Retry(redirect=2, raise_on_redirect=False))

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True

        print
        text = text_maker.handle(str(r.data.decode()))    #html to text
        splitted_text = text.split()

        final_text = []
        for i in splitted_text:             #clear the text
            temp = re.sub("[^A-Za-z]", "", i)
            if (temp != ''):
                final_text.append(temp)

        return " ".join(final_text)         #make the array text again
    except ( urllib3.exceptions.MaxRetryError) as e:
        pass
    # text_maker = html2text.HTML2Text()
    # text_maker.ignore_links = True
    # text_maker.ignore_images = True

    # text = text_maker.handle(r.text)    #html to text
    # splitted_text = text.split()

    # final_text = []
    # for i in splitted_text:             #clear the text
    #     temp = re.sub("[^A-Za-z]", "", i)
    #     if (temp != ''):
    #         final_text.append(temp)

    # return " ".join(final_text)         #make the array text again

bookmarks = getBookmarks()

# text = filteredText(bookmarks[0])
# print(text)

for bookmark in bookmarks:
    
    text = filteredText(bookmark)
    print(text)

    # time.sleep( 0.250 )