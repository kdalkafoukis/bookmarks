#!/usr/bin/env python3.7

from pathlib import Path
import json
from objectpath import Tree
from os import getcwd
from shutil import copyfile

def getBookmarks(browser):
        if (browser == "chrome"):
                filepath = chromeBookmarks()
                bookmarks = readFile(filepath)
        else:
                bookmarks = []
                
        return bookmarks 

def chromeBookmarks():
        # maybe check for day file modified to update it
        file_chrome = str(Path.home()) + '/Library/Application Support/Google/Chrome/Default/Bookmarks' #mac
        # file_chrome = str(Path.home()) + '/.config/google-chrome/Default/Bookmarks' #ubuntu
        file_path_src = Path(file_chrome)
        file_path_dst = Path(getcwd() + '/bookmarks.json')
        if not file_path_dst.is_file() and file_path_src.is_file():
                copyfile(file_path_src, file_path_dst)

        res = file_path_dst
        return res

def readFile(filepath):
        try:
                with open(filepath) as f:
                        jsondata = json.load(f)
                        data = arrayOfBookmarks(jsondata)
                        return data
        except:
                return []

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