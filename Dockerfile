FROM ubuntu 

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install python3.7 -y

RUN apt-get install curl -y
RUN apt-get install vim -y 

RUN apt install python3-pip -y
RUN pip3 install pipenv

ADD ./ /app
WORKDIR /app

RUN pipenv install --python 3.7

RUN pipenv run test

EXPOSE 8080