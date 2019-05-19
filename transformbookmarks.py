#!/usr/bin/env python3.7

import requests
import html2text
import re

from config import config

def transformBookmarks(url):
    return fetchAndFilterText(url)

def aggregateSameWords(text):
    obj = {}    # keys the words, values the num of showed word in the text
    for word in text:
        if word not in obj:
            obj[word] = 1
        else:
            obj[word] = obj[word] + 1
    return obj

def fetchAndFilterText(url): #take a website and tranform it to text
    try:
        r = requests.get(url,verify= False)   #make the request

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True

        text = text_maker.handle(r.text)    #html to text
        splitted_text = text.split()

        final_text = []
        for i in splitted_text:             #clear the text
            temp = re.sub(config['re_rule'], "", i)
            if (temp != ''):
                res = temp
                if (config['lowercase']==True):
                    res = temp.lower()    #new addition
                final_text.append(res)

        # res = " ".join(final_text)  #make the array text again
        # res = final_text
        res = aggregateSameWords(final_text)
        return res    
    except requests.exceptions.RequestException:
        pass
