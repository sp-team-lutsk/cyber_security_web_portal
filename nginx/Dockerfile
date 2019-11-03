FROM nginx:1.17

RUN rm -rf /usr/share/nginx/html/*

# copy nginx config
COPY ./config/nginx.conf /etc/nginx/nginx.conf
# copy static files
COPY --from=node /app/dist/frontend/ /usr/share/nginx/html

# copy certificates
# COPY ./certificates/nginx.crt /etc/nginx/ssl/nginx.crt
# COPY ./certificates/nginx.key /etc/nginx/ssl/nginx.key

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
