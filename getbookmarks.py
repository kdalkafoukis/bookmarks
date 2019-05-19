#!/usr/bin/env python3.7

from pathlib import Path
import json
from objectpath import Tree
import os

def getBookmarks(browser):
        if (browser == "chrome"):
                filepath = chromeBookmarks()
                bookmarks = readFile(filepath)
        else:
                bookmarks = []
                
        return bookmarks 

def chromeBookmarks():
        # if pwd and file with bookmarks exist return it else create 
        # a file and copy it from the original filepath 
        # (maybe check for day file modified to update it)
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