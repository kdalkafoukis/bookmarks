# bookmarks ![TravisCI status](https://travis-ci.org/kdalkafoukis/bookmarks.svg?branch=master)  


### git  
- install [git](https://git-scm.com/downloads)
- `git clone git@github.com:kdalkafoukis/bookmarks.git`

### travis  
- install [travis](https://docs.travis-ci.com/user/languages/python/) for python

### install app  

- install [python3.7](https://www.python.org/) and [pipenv](https://docs.pipenv.org/en/latest/install/#installing-pipenv)
- `pipenv install --python 3.7`
- `pipenv shell`  

test insert one bookmark to test db in mongo db
- `pipenv run test_init_bookmarks`  

insert all bookmarks to mongo db
- `pipenv run init_bookmarks`

find a test bookmark  
- `pipenv run test_find_bookmark`

### set up mongo db  

[official mongodb docker](https://hub.docker.com/_/mongo)

- `docker pull mongo`
- `docker run --name mongo -p 27017:27017 -d mongo`
- `docker restart mongo`


### build docker

- `docker build -t bookmarks .`