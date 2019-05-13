#!/usr/bin/env python3.7

from pathlib import Path
import json
from objectpath import *

def main():
    return chromeBookmarks()

def chromeBookmarks():
    linux_chrome_file = str(Path.home())+'/.config/google-chrome/Default/Bookmarks'

    with open(linux_chrome_file) as f:
        data = json.load(f)
        jsonnn_tree = Tree(data)

        bookmarks = tuple(jsonnn_tree.execute('$..url')) #search for url key and put the results in a tuple
        print(bookmarks)
        return bookmarks , len(bookmarks)

if __name__ == "__main__":
    main()


