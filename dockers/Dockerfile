FROM centos:8

RUN mkdir -p /opt/monitor-ecs
WORKDIR /opt/monitor-ecs

RUN yum install python3 python3-devel python3-pip rrdtool.x86_64 -y
RUN dnf groupinstall "Development Tools" -y
RUN rpm -Uvh http://mirror.centos.org/centos/8/PowerTools/x86_64/os/Packages/rrdtool-devel-1.7.0-16.el8.x86_64.rpm
ADD python-requirements.txt /tmp
RUN pip3 install -r /tmp/python-requirements.txt
RUN dnf groupremove "Development Tools" -y


ADD ./ /opt/monitor-ecs/

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]