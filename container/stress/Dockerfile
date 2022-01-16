# use python 3.8 image (https://hub.docker.com/_/python)
FROM python:3.8

# set working directory of a docker container to /src
WORKDIR /src

# copy directories and files from ./src/ to docker container of a working directory
COPY ./src/ .

# execute command to change file permission for /var/www/html/ recursively to rwxrwxr--
# RUN chmod +x /src/run.sh

# execute command to install required python library
RUN pip install -r requirements.txt

# run stress test script
# ARG TOTAL_REQUEST
# ARG TOTAL_CONNECTION
# ARG URL

# ENV ENV_TOTAL_REQUEST=$TOTAL_REQUEST
# ENV ENV_TOTAL_CONNECTION=$TOTAL_CONNECTION
# ENV ENV_URL=$URL

# ENTRYPOINT ["/src/run.sh"]