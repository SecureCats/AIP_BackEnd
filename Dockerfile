FROM python:3.7
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

# Use sed because of potential file owner issue
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org/debian-security|mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org|mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt --no-cache-dir && \
    rm -rf /var/lib/apt/lists/* && \
    echo "daemon off;" >> /etc/nginx/nginx.conf && \
    python manage.py collectstatic --noinput
ENV DEBUG False
COPY deploy/nginx-app.conf /etc/nginx/sites-available/default
COPY deploy/supervisor-app.conf /etc/supervisor/conf.d/
EXPOSE 80
ENTRYPOINT [ "/bin/bash", "deploy/entrypoint.sh" ]
CMD ["supervisord", "-n"]