#!/usr/bin/python3

import boto3
from datetime import datetime, timedelta
from pytz import timezone
import sqlite3

class Monitor(object):
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

        try:
            self.conn = sqlite3.connect(self.sqlitedb)
        except Error as e:
            print(e)

    def _setCloudWatchDimensions(self):
        dimension = {
            'Namespace' : '',
            'MetricName' : '',
            'Dimensions' : [],
        }
        dimension['Namespace'] = 'AWS/ECS'
        dimension['MetricName'] = 'CPUUtilization'
        dimension['Dimensions'].append({'Name': 'ClusterName', 'Value': self.cluster})
        dimension['Dimensions'].append({'Name': 'ServiceName', 'Value': self.service})
        return dimension

    def getCPU(self):
        dimension = self._setCloudWatchDimensions()
        NowTime = self.now_timezone - timedelta(minutes=0) 
        response = self.cloudwatch.get_metric_statistics(
            Namespace = dimension['Namespace'],
            MetricName = dimension['MetricName'],
            Dimensions = dimension['Dimensions'],
            StartTime = self.now_timezone - timedelta(minutes=5),
            EndTime = NowTime,
            Period = 300,
            Statistics = ['Average'],
            Unit = 'Percent'
        )
        return {'date': NowTime , 'cpu': round(response['Datapoints'][0].get('Average'),2)}

    def getTasksCount(self):
        response = self.ecs.describe_services(
            cluster = self.cluster,
            services = [self.service])
        return response.get('services')[0].get('runningCount')

    def saveData(self,data,taskscount):
        fmt = "%Y-%m-%d %H:%M:%S"
        cpudata = (data.get('date').strftime(fmt), data.get('cpu', 0), taskscount)
        sql = ''' INSERT INTO ecs_cluster_blocs_pro(TIME,CPU,TASKCOUNT)
              VALUES(?,?,?) '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, cpudata)
            self.conn.commit()
        except sqlite3.Error as error:
            print("{} {}".format(self.now_timezone.strftime(fmt), error))

if __name__ == '__main__':
    ClodWatch = Monitor()
    taskscount = ClodWatch.getTasksCount()
    data = ClodWatch.getCPU()
    ClodWatch.saveData(data, taskscount)
    


