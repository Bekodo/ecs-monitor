import settings
from functions import periods, metrics, services, createrrdimagecpu, createrrdimagemem, createrrdimagetask
from flask import Flask, render_template, send_file, request
from flask_httpauth import HTTPBasicAuth
import rrdtool
import tempfile
from datetime import datetime
from pytz import timezone
from pprint import pprint

app = Flask(__name__,static_url_path='/ecs/monitor/static')
auth = HTTPBasicAuth()

@app.route('/ecs/monitor/img/<service>/<metric>/<period>')
<<<<<<< HEAD
def rrdimage(service, metric, period):
=======
def chartimage(service, metric, period):
    period = (period if period in periods else '1d')
    metric = (metric if metric in metrics else 'cpu')
    service = (service if service in services else 'blocs-pro')
    rrdfile = settings.RRDPATH + service + '_ecs_mem_cpu_task.rrd'

>>>>>>> 01b7e050f9da84e9ab7558982d5ed102268544cc
    fmt = "%d-%m-%Y %H\:%M"
    stimezone = 'Europe/Dublin'
    tsdate = datetime.fromtimestamp(rrdtool.last(rrdfile))
    amsterdam_tz = timezone('Europe/Amsterdam')
    now_tz = amsterdam_tz.localize(tsdate)
    dublin_tz = timezone(stimezone)
    now_timezone = now_tz.astimezone(dublin_tz)
    strdate = now_timezone.strftime(fmt)

<<<<<<< HEAD
    rrdfile = settings.RRDPATH + service + '_ecs_mem_cpu_task.rrd'

=======
>>>>>>> 01b7e050f9da84e9ab7558982d5ed102268544cc
    if (metric == 'cpu'):
        filename = createrrdimagecpu(rrdfile, service, period, strdate)
    elif (metric == 'mem'):
        filename = createrrdimagemem(rrdfile, service, period, strdate)
    elif (metric == 'task'):
        filename = createrrdimagetask(rrdfile, service, period, strdate)
    else:
        filename = createrrdimagecpu(rrdfile, service, period, strdate)
    return send_file(filename, mimetype='image/png', cache_timeout=-1)
    
@app.route('/ecs/monitor/services/<service>/')
def sercices(service):
    return render_template('services.html', metrics=settings.METRICS, services=settings.SERVICES, periods=settings.PRERIODS, service=service, username=auth.username())

@app.route('/ecs/monitor/metrics/<metric>/')
def metrics(metric):
    return render_template('metrics.html', metrics=settings.METRICS, services=settings.SERVICES, periods=settings.PRERIODS, metric=metric, username=auth.username())

@app.route('/ecs/monitor/service-metric/<service>/<metric>/')
def sercicesmetric(service,metric):
    return render_template('service-metric.html', metrics=settings.METRICS, services=settings.SERVICES, periods=settings.PRERIODS, metric=metric, service=service, username=auth.username())

@app.route('/ecs/monitor/')
def index():
    return render_template('index.html', metrics=settings.METRICS, services=settings.SERVICES, username=auth.username())

