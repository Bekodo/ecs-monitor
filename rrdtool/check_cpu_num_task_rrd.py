#!/opt/local/bin/python

import boto3
from datetime import datetime, timedelta
from pytz import timezone
import rrdtool

class Monitor(object):
    stimezone = 'Europe/Dublin'
    rrdfile = 'ecs_mem_cpu_task.rrd'
    profile = 'defautl' #Added for setup
    region = 'eu-west-1' #Added for setup
    stimezone = 'Europe/Dublin' #Added for setup
    sqlitedb = 'ecs_cluster.db' #Added for setup
    cluster = '' #Added for setup
    service = '' #Added for setup
    arn = '' #Added for setup
    conn = None
    now_timezone = None

    def __init__(self):

        now_utc = datetime.now()
        amsterdam_tz = timezone('Europe/Amsterdam')
        now_tz = amsterdam_tz.localize(now_utc)
        dublin_tz = timezone(self.stimezone)
        self.now_timezone = now_tz.astimezone(dublin_tz)
        
        session = boto3.Session(profile_name = self.profile)
        self.cloudwatch = session.client('cloudwatch',region_name = self.region)
        self.ecs = session.client('ecs',region_name = self.region)

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

    def saveData(self,data):
        rawdata = {'cpu': data.get('cpu', 0).get('CPUUtilization'), 'mem': data.get('mem', 0).get('MemoryUtilization'), 'task': data.get('tasks', 0)}
        data = 'N:' + str(rawdata.get('cpu')) +":"+ str(rawdata.get('mem')) +":"+ str(rawdata.get('task'))
        result = rrdtool.updatev(self.rrdfile, data)

if __name__ == '__main__':
    ClodWatch = Monitor()
    data = {}  
    data['tasks'] = ClodWatch.getTasksCount()
    data['cpu'] = ClodWatch.getMetric('CPUUtilization')
    data['mem'] = ClodWatch.getMetric('MemoryUtilization')
    ClodWatch.saveData(data)