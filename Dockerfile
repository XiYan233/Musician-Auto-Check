FROM ubuntu:20.04

WORKDIR /root/MusicianAutoCheck/

RUN apt-get update -y && apt-get install wget git -y && apt-get install pip -y && pip install requests

ADD config.ini config.ini

ADD main.py main.py

ADD start.sh start.sh

