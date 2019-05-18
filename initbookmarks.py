from getbookmarks import getBookmarks
from transformbookmarks import transformBookmarks
from createbookmarksdb import insertDocument

def testInsertOne():
    url = bookmarks[0]['url']
    text = transformBookmarks(url)
    bookmarks[0]["text"] = text

    insertDocument(bookmarks[0])
    print(bookmarks[0])


def insertAll():
    for bookmark in bookmarks:
        url = bookmark['url']
        text = transformBookmarks(url)
        bookmark["text"] = text
        insertDocument(bookmark)

bookmarks = getBookmarks("chrome")
insertAll()