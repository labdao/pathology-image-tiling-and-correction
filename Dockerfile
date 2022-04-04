# choose a base image, we use a lightweight docker container running python3 on ubuntu
FROM ubuntu:jammy 
# install basic packages
RUN apt-get update
RUN apt-get install -y tmux wget curl git nano
RUN apt-get install -y python3 pip
# copy the current repository to the container and store it at /usr/src/app - you can learn more about this convention here: https://en.wikipedia.org/wiki/Unix_filesystem#Conventional_directory_layout
COPY . /usr/src/app
# install the dependencies
RUN pip install -r /usr/src/app/requirements.txt 
# open a shell when launching the container
CMD ["bash"] 