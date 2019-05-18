#!/usr/bin/env python3.7

from pathlib import Path
import json
from objectpath import Tree
import os

def getBookmarks():
        filepath = chromeBookmarks()
        bookmarks = readFile(filepath)
        # print(bookmarks)
        return bookmarks 

def chromeBookmarks():
        return str(Path.home())+'/.config/google-chrome/Default/Bookmarks'

def readFile(filepath):
        with open(filepath) as f:
                jsondata = json.load(f)
                data = arrayOfBookmarks(jsondata)
                return data

def arrayOfBookmarks(data):
        jsonnn_tree = Tree(data)
        bookmarks = list(jsonnn_tree.execute('$..*'))  # flat the tree
        filteredBookmarks = []
        keysToMatch = ("name","url","date_added","id","meta_info")
        for bookmark in bookmarks:  # search it
                obj = {}        
                if all (key in bookmark for key in keysToMatch):  # filter keys
                        for k in keysToMatch:
                                obj[k] = bookmark[k]
                        filteredBookmarks.append(obj)  # add the object with keys

        return filteredBookmarks   

if __name__ == "__main__":
        getBookmarks()