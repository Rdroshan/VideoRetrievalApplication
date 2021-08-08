FROM python:3.7-alpine

# root directory
RUN mkdir /video_api

# copy the current directory contents make sure to be in root directory
COPY requirements  /video_api/
COPY api /video_api/api/


# set work directory
WORKDIR /video_api/

# set your api keys enviroment variables
ENV GOOGLE_API_KEYS=""

# install requirements 
RUN pip install -r requirements.txt

