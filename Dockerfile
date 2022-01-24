FROM alpine:3.11

WORKDIR /server
COPY "./" "./"
EXPOSE 5000

RUN echo 'https://mirrors.aliyun.com/alpine/v3.11/main/' >/etc/apk/repositories && \
    echo 'https://mirrors.aliyun.com/alpine/v3.11/community/' >>/etc/apk/repositories && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&  \
    echo "Asia/Shanghai" >/etc/timezone

RUN apk add --no-cache --virtual=.build_dependencies python3-dev musl-dev libevent-dev  py3-cffi linux-headers  openssl-dev libxslt libxslt-dev g++ libressl-dev && \
    apk add --no-cache  tzdata postgresql-dev gcc libffi-dev zeromq-dev yasm ffmpeg make wget && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install  -i https://mirrors.aliyun.com/pypi/simple/ --no-cache pip --upgrade setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    pip3 install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir

CMD python ./run.py