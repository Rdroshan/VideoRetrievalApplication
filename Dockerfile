FROM ubuntu:20.04
RUN apt update && apt-get -y install cron libpq-dev gcc python3-pip python3.7

# root directory
RUN mkdir /video_api

# copy the current directory contents make sure to be in root directory
COPY requirements.txt  /video_api/
COPY api /video_api/api/
#COPY variables.sh /video_api/

# Cron setup
#COPY crontab /etc/cron.d/cron-tab
#RUN chmod 0644 /etc/cron.d/cron-tab

# Create file for logging
RUN touch /tmp/debug.log

# set work directory
WORKDIR /video_api/

# install requirements 
RUN pip install -r requirements.txt

