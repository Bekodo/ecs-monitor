import settings
from functions import periods, metrics, services, createrrdimagecpu, createrrdimagemem, createrrdimagetask
from flask import Flask, render_template, send_file, request
from flask_httpauth import HTTPBasicAuth
import rrdtool
import datetime
from pytz import timezone
from pprint import pprint

app = Flask(__name__,static_url_path='/ecs/monitor/static')
auth = HTTPBasicAuth()

@app.route('/ecs/monitor/img/<service>/<metric>/<period>')
def chartimage(service, metric, period):
    fmt = "%d-%m-%Y %H\:%M"
    stimezone = 'Europe/Dublin'
    now_utc = datetime.datetime.now()
    amsterdam_tz = timezone('Europe/Amsterdam')
    now_tz = amsterdam_tz.localize(now_utc)
    dublin_tz = timezone(stimezone)
    now_timezone = now_tz.astimezone(dublin_tz)
    strdate = now_timezone.strftime(fmt)

    period = (period if period in periods else '1d')
    metric = (metric if metric in metrics else 'cpu')
    service = (service if service in services else 'blocs-pro')
    rrdfile = settings.RRDPATH + service + '_ecs_mem_cpu_task.rrd'

    if (metric == 'cpu'):
        filename = createrrdimagecpu(rrdfile, period, strdate)
    elif (metric == 'mem'):
        filename = createrrdimagemem(rrdfile, period, strdate)
    elif (metric == 'task'):
        filename = createrrdimagetask(rrdfile, period, strdate)
    else:
        filename = createrrdimagecpu(rrdfile, period, strdate)
    return send_file(filename, mimetype='image/png', cache_timeout=-1)
    
@app.route('/ecs/monitor/<service>/<metric>')
def chartpage(service, metric):
    return render_template('metric.html', metrics=settings.METRICS, services=settings.SERVICES, periods=settings.PRERIODS, metric=metric, service=service, username=auth.username())

@app.route('/ecs/monitor/')
def index():
    return render_template('index.html', metrics=settings.METRICS, services=settings.SERVICES, username=auth.username())

