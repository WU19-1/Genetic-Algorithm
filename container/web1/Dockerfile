# use python 3.8 image (https://hub.docker.com/_/php)
FROM php:7.4-apache

# open port 80 when the container is running
EXPOSE 80

# copy directories and files from ./src/ to /var/www/html/
COPY ./src/ /var/www/html/

# execute command to add user and group named www-data
RUN adduser www-data www-data

# execute command to change file owner for /var/www/html/ recursively to www-data
RUN chown --recursive www-data:www-data /var/www/html/

# execute command to change file permission for /var/www/html/ recursively to rwxrwxr--
RUN chmod --recursive 774 /var/www/html/
