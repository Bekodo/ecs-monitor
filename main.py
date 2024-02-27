import settings
from functions import periods, metrics, services, createrrdimagecpu, createrrdimagemem, createrrdimagetask, static_createrrdimagecpu, static_createrrdimagemem, static_createrrdimagetask
from flask import Flask, render_template, send_file, request
from flask_httpauth import HTTPBasicAuth
from os import path, getcwd
import os
import click


app = Flask(__name__,static_url_path='/ecs/monitor/static')
auth = HTTPBasicAuth()

filepath = path.abspath(getcwd())
static = os.getenv('STATIC', False)

@app.route('/ecs/monitor/img/<service>/<metric>/<period>')
def rrdimage(service, metric, period):
    rrdfile = filepath + settings.RRDPATH + service + '_ecs_mem_cpu_task.rrd'

    if static: 
        if (metric == 'cpu'):
            filename = static_createrrdimagecpu(service, period)
        elif (metric == 'mem'):
            filename = static_createrrdimagemem(service, period)
        elif (metric == 'task'):
            filename = static_createrrdimagetask(service, period)
    else:
        if (metric == 'cpu'):
            filename = createrrdimagecpu(rrdfile, service, period)
        elif (metric == 'mem'):
            filename = createrrdimagemem(rrdfile, service, period)
        elif (metric == 'task'):
            filename = createrrdimagetask(rrdfile, service, period)
        
    return send_file(filename, mimetype='image/png')
    
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
    return render_template('index.html', metrics=settings.METRICS, services=settings.SERVICES, favorites=settings.FAVORITES, username=auth.username())

@app.cli.command('generatecpu')
@click.argument('service')
@click.argument('period')
def generatecpu(service, period):
    rrdfile = filepath + settings.RRDPATH + service + '_ecs_mem_cpu_task.rrd'
    createrrdimagecpu(rrdfile, service, period)

@app.cli.command('generatemem')
@click.argument('service')
@click.argument('period')
def generatemem(service, period):
    rrdfile = filepath + settings.RRDPATH + service + '_ecs_mem_cpu_task.rrd'
    createrrdimagemem(rrdfile, service, period)

@app.cli.command('generatetask')
@click.argument('service')
@click.argument('period')
def generatetask(service, period):
    rrdfile = filepath + settings.RRDPATH + service + '_ecs_mem_cpu_task.rrd'
    createrrdimagetask(rrdfile, service, period)

