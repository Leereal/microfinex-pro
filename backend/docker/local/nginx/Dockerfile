FROM nginx:1.23.3-alpine

#Let's remove the default config file
RUN rm /etc/nginx/conf.d/default.conf

#Copy the custom config file from the current directory to the location specified in the Dockerfile
COPY ./default.conf /etc/nginx/conf.d/default.conf