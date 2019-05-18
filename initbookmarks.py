from getbookmarks import getBookmarks
from transformbookmarks import transformBookmarks

bookmarks = getBookmarks("chrome")

# for bookmark in bookmarks:
#     url = bookmark['url']
#     text = transformBookmarks(url)

url = bookmarks[0]['url']
text = transformBookmarks(url)

print(text)