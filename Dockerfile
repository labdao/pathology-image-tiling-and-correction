# choose a base image, we use a lightweight docker container running python3 on ubuntu
FROM ubuntu:jammy 
FROM python:3.7
# had to specify python version because 3.10 isn't compatible with packages, and is the default

# install basic packages
RUN apt-get update
RUN apt-get install -y tmux wget curl git nano
RUN apt-get install ffmpeg libsm6 libxext6  -y 
# Added above line because (https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo)
# RUN apt-get install -y pip
# copy the current repository to the container and store it at /usr/src/app - you can learn more about this convention here: https://en.wikipedia.org/wiki/Unix_filesystem#Conventional_directory_layout
COPY . /usr/src/app
# install the dependencies
RUN pip install -r /usr/src/app/requirements.txt 
# open a shell when launching the container
CMD ["bash"] 