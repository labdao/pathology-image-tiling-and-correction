# syntax=docker/dockerfile:1

# choose a base image, we use a lightweight docker container running python3 on ubuntu
FROM --platform=linux/amd64 python:3.7
# had to specify python version because 3.10 isn't compatible with packages, and is the default

# Maybe this can be tensorflow in the future to support Coral TPUs?
ENV DGLBACKEND=pytorch

# install basic packages
RUN apt-get update
RUN apt-get install -y tmux wget curl git nano
RUN apt-get install -y ffmpeg libsm6 libxext6
# Added above line because (https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo)

# copy the current repository to the container and store it at /src
WORKDIR /src
COPY requirements.txt /src/
# install the dependencies
RUN pip install -r /src/requirements.txt 
# transfer rest of data - separating the requirment install from the rest of the data can save time when building the image
COPY . /src/
# expose port for FastAPI
EXPOSE 8000
# listen for requests when launched
CMD ["/bin/bash", "-c", "uvicorn main:app --reload --host \"0.0.0.0\" --port 8000"] 
