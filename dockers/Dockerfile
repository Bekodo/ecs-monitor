FROM python:3.9.18

RUN mkdir -p /opt/monitor-ecs
WORKDIR /opt/monitor-ecs

RUN apt update
RUN apt install -y librrd-dev
ADD . /opt/monitor-ecs
RUN pip install -r /opt/monitor-ecs/dockers/python-requirements.txt

EXPOSE 5000
CMD ["/usr/bin/flask", "run", "--host=0.0.0.0"]
