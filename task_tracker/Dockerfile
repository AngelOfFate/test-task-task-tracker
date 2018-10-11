FROM python:3.6.3

EXPOSE 8000

RUN mkdir /var/task_tracker
RUN mkdir /var/log/task_tracker

WORKDIR /opt/task_tracker
COPY . /opt/task_tracker

RUN pip install -r requirements.txt

COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

