#!/opt/local/bin/python3.7

import multiprocessing
import configparser
import time
import os
import pathlib
import boto3
from datetime import datetime, timedelta
from pytz import timezone
import rrdtool

from pprint import pprint

class Monitor(object):
    stimezone = 'Europe/Dublin'
    rrdfile = ''
    stimezone = 'Europe/Dublin' #Added for setup
    cluster = '' #Added for setup
    service = '' #Added for setup
    arn = '' #Added for setup
    now_timezone = None

    def __init__(self, key, secretkey, region, service, cluster, arn, rrdfile):
        self.service = service
        self.cluster = cluster
        self.asrn = arn
        now_utc = datetime.now()
        amsterdam_tz = timezone('Europe/Amsterdam')
        now_tz = amsterdam_tz.localize(now_utc)
        dublin_tz = timezone(self.stimezone)
        self.now_timezone = now_tz.astimezone(dublin_tz)
        self.rrdfile = rrdfile
        
        self.cloudwatch = boto3.client('cloudwatch',
            aws_access_key_id = key,
            aws_secret_access_key = secretkey,
            region_name = region)
        self.ecs = boto3.client('ecs',
            aws_access_key_id = key,
            aws_secret_access_key = secretkey,
            region_name = region)

    def _setCloudWatchDimensions(self):
        dimension = {
            'Namespace' : '',
            'MetricName' : '',
            'Dimensions' : [],
        }
        dimension['Namespace'] = 'AWS/ECS'
        dimension['Dimensions'].append({'Name': 'ClusterName', 'Value': self.cluster})
        dimension['Dimensions'].append({'Name': 'ServiceName', 'Value': self.service})
        return dimension

    def getMetric(self,metric):
        dimension = self._setCloudWatchDimensions()
        NowTime = self.now_timezone - timedelta(minutes=0) 
        response = self.cloudwatch.get_metric_statistics(
            Namespace = dimension['Namespace'],
            MetricName = metric,
            Dimensions = dimension['Dimensions'],
            StartTime = self.now_timezone - timedelta(minutes=5),
            EndTime = NowTime,
            Period = 300,
            Statistics = ['Average'],
            Unit = 'Percent'
        )
        return {'date': NowTime , metric: round(response['Datapoints'][0].get('Average'),2)}

    def getTasksCount(self):
        response = self.ecs.describe_services(
            cluster = self.cluster,
            services = [self.service])
        return response.get('services')[0].get('runningCount')

    def __createRRD(self, rrdfile):
        rrdtool.create(rrdfile,
            "--step", "300",
            "--start", "now",
            "DS:cpu:GAUGE:600:0:U",
            "DS:mem:GAUGE:600:0:U",
            "DS:task:GAUGE:600:0:U",
            "RRA:AVERAGE:0.5:1:288",
            "RRA:MIN:0.5:1:288",
            "RRA:MAX:0.5:1:288",
            "RRA:LAST:0.5:1:288",
            "RRA:AVERAGE:0.5:3:672",
            "RRA:MIN:0.5:3:672",
            "RRA:MAX:0.5:3:672",
            "RRA:LAST:0.5:3:672",
            "RRA:AVERAGE:0.5:12:744",
            "RRA:MIN:0.5:12:744",
            "RRA:MAX:0.5:12:744",
            "RRA:LAST:0.5:12:744",
            "RRA:AVERAGE:0.5:72:1460",
            "RRA:MIN:0.5:72:1460",
            "RRA:MAX:0.5:72:1460",
            "RRA:LAST:0.5:72:1460")

    def saveData(self,data):
        rawdata = {'cpu': data.get('cpu', 0).get('CPUUtilization'), 'mem': data.get('mem', 0).get('MemoryUtilization'), 'task': data.get('tasks', 0)}
        data = 'N:' + str(rawdata.get('cpu')) +":"+ str(rawdata.get('mem')) +":"+ str(rawdata.get('task'))
        try:
            result = rrdtool.update(self.rrdfile, data)
        except rrdtool.OperationalError as e:
            self.__createRRD(rrdfile)
            result = rrdtool.update(self.rrdfile, data)

def worker(key, secretkey, region, service, cluster, arn, rrdfile):
    ClodWatch = Monitor(key, secretkey, region, service, cluster, arn, rrdfile)
    data = {}  
    data['tasks'] = ClodWatch.getTasksCount()
    data['cpu'] = ClodWatch.getMetric('CPUUtilization')
    data['mem'] = ClodWatch.getMetric('MemoryUtilization')
    ClodWatch.saveData(data)

if __name__ == '__main__':
    
    currentdir = pathlib.PurePosixPath(os.path.dirname(os.path.realpath(__file__)))
    rootdir = currentdir / '..'
    rrddir = rootdir / 'rrd'
    rrdfile = ''
    if not os.path.exists(rrddir):
        os.makedirs(rrddir)

    inifile = currentdir / 'config.ini'
    parser = configparser.ConfigParser()
    parser.read(inifile)

    for section_name in parser:
        section = parser[section_name]
        if section_name is not 'DEFAULT':
            for name in section:
                if name == 'key':
                    key = section[name]
                if name == 'secretkey':
                    secretkey = section[name]
                if name == 'region':
                    region = section[name]
                if name == 'service':
                    service = section[name]
                if name == 'cluster':
                    cluster = section[name]
                if name == 'arn':
                    arn = section[name]
            rrdfile = str(rrddir) + '/' + service + '_ecs_mem_cpu_task.rrd'
            jobs = []
            p = multiprocessing.Process(target=worker, args=(key, secretkey, region, service, cluster, arn, rrdfile))
            jobs.append(p)
            p.start()

