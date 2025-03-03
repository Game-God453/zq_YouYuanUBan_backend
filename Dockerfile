# Django
FROM python:3.11-buster
#ENV PYTHONUNBUFFERED=1

# 接收构建参数
ARG USER_ID
ARG GROUP_ID

# 创建匹配宿主机用户的用户
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -u ${USER_ID} -g appuser -s /bin/sh appuser

# 设置工作目录并修正权限
RUN mkdir -p /etc/uwsgi/django && \
    chown -R ${USER_ID}:${GROUP_ID} /etc/uwsgi

# 切换到非root用户
USER appuser
RUN chown -x 775 ./start.sh

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y vim
WORKDIR /etc/uwsgi/django
RUN python3 -m pip install uwsgi uwsgi-tools -i https://pypi.tuna.tsinghua.edu.cn/simple/
ADD requirements.txt /etc/uwsgi/django/requirements.txt
RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

CMD uwsgi --ini /etc/uwsgi/django/uwsgi.ini

#ADD uwsgi.ini uwsgi.ini
#ADD . /etc/uwsgi/django
#EXPOSE 8086
#CMD uwsgi --ini /etc/uwsgi/django/uwsgi.ini
#采用卷挂载，在docker-compose.yml文件中配置