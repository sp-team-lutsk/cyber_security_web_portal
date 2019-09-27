FROM nginx:1.17

# copy nginx config
COPY ./config/nginx.conf /etc/nginx/nginx.conf

# copy static files
COPY --from=node /usr/src/app/ /usr/share/nginx/html

# copy certificates
# COPY ./certificates/nginx.crt /etc/nginx/ssl/nginx.crt
# COPY ./certificates/nginx.key /etc/nginx/ssl/nginx.key

EXPOSE 80 443

ENTRYPOINT ["nginx"]

CMD ["-g", "daemon off;"]
