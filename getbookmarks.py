#!/usr/bin/env python3.7

from pathlib import Path
import json
from objectpath import Tree
import os

def getBookmarks():
        filepath = chromeBookmarks()
        bookmarks = readFile(filepath)
        return bookmarks

def chromeBookmarks():
        return str(Path.home())+'/.config/google-chrome/Default/Bookmarks'

# connected to the chromeBookmarks
def readFile(filepath):
        with open(filepath) as f:
                data = json.load(f)
                jsonnn_tree = Tree(data)

                bookmarks = tuple(jsonnn_tree.execute('$..url')) #search for url key and put the results in a tuple
                return bookmarks
                
def printBookmarks():
        bookmarks = getBookmarks()
        print(bookmarks)

def writeFile():
        bookmarks = getBookmarks()
        json_file = 'bookmarks.txt'
        with open(json_file,'w') as f:
                f.write(str(bookmarks))

if __name__ == "__main__":
        getBookmarks()