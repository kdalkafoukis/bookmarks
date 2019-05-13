#!/usr/bin/env python3.7

from pathlib import Path
import json
from objectpath import *
import os

def main():
    filepath = chromeBookmarks()
    bookmarks = readFile(filepath)

    printBookmarks(bookmarks)
    
    json_file = 'bookmarks.txt'
    writeFile(json_file,bookmarks)

def chromeBookmarks():
    return str(Path.home())+'/.config/google-chrome/Default/Bookmarks'

def printBookmarks():
    print(bookmarks)

def readFile(filepath):
     with open(filepath) as f:
        data = json.load(f)
        jsonnn_tree = Tree(data)

        bookmarks = tuple(jsonnn_tree.execute('$..url')) #search for url key and put the results in a tuple
        return bookmarks

def writeFile(filepath,bookmarks):
    with open(filepath,'w') as f:
        f.write(str(bookmarks))

if __name__ == "__main__":
    main()


