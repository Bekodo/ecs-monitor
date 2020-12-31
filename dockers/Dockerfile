FROM centos:8

RUN mkdir -p /opt/monitor-ecs
WORKDIR /opt/monitor-ecs

RUN yum install python3 python3-devel python3-pip -y
ADD python-requirements.txt /tmp
RUN pip3 install -r /tmp/python-requirements.txt

ADD ./ /opt/monitor-ecs/

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]