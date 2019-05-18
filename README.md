# bookmarks

### install app

- install python3.7 and pipenv
- `pipenv install --python 3.7`
- `pipenv shell`
- `python initbookmarks.py`

### set up mongo db

[official mongodb docker](https://hub.docker.com/_/mongo)

- `docker pull mongo`
- `docker run --name mongo -p 27017:27017 -d mongo`
- `docker restart mongo`