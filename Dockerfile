FROM python:3.8-alpine
RUN echo -e http://mirrors.ustc.edu.cn/alpine/v3.16/main/ > /etc/apk/repositories & apk update & apk add --no-cache --virtual .build-deps gcc g++ build-base freetype-dev libxml2-dev libxslt-dev openssl openssl-dev libffi libffi-dev gmp gmp-dev sqlite sqlite-dev

RUN mkdir -p /data/www/newkeeper
ADD . /data/www/newkeeper
WORKDIR /data/www/newkeeper/newton

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python manage.py migrate
CMD ["sh", "/data/www/newkeeper/entrypoint.sh"]
