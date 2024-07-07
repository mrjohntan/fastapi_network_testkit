FROM nginx:mainline
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
COPY app.conf /etc/nginx/conf.d/
COPY demo-index.html /usr/share/nginx/html